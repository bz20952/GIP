import numpy as np
from scipy import linalg
import vals
from matplotlib import pyplot as plt
import smoa
import pandas as pd
from scipy.integrate import solve_ivp
import plot as p
import sympy as sp
from scipy.interpolate import interp1d


def mass_mat(L):

    return np.array([
        [ 156, 22*L, 54, -13*L],
        [ 22*L, 4*L**2, 13*L, -3*L**2],
        [ 54, 13*L, 156, -22*L],
        [-13*L, -3*L**2, -22*L, 4*L**2]
    ])


def stiffness_mat(L):

    return np.array([
        [12, 6*L, -12 , 6*L],
        [6*L, 4*L**2, -6*L, 2*L**2],
        [-12, -6*L, 12, -6*L],
        [6*L, 2*L**2, -6*L, 4*L**2]
    ])


def fe(n_nodes: int):

    n_dofs = 2*n_nodes
     
    # Element 1
    L_1 = vals.L/(n_nodes-1)
    I_1, A_1 = smoa.hollow_rect_beam(vals.b, vals.h, vals.b_inner, vals.h_inner)
    M_1 = ((vals.density * A_1 * L_1)/420) * mass_mat(L_1)
    K_1 = ((vals.E*I_1)/(L_1**3)) * stiffness_mat(L_1)

    # Assemble matrices
    M = np.zeros((n_dofs,n_dofs))
    K = np.zeros((n_dofs,n_dofs))
    for i in range(0, n_dofs-2, 2):
        M[i:i+4,i:i+4] += M_1
        K[i:i+4,i:i+4] += K_1

    # print("Mass matrix:\n", M)
    # print("Stiffness matrix:\n", K)

    # # Apply simply-supported BCs
    # M = np.delete(M, 0, axis=0)
    # M = np.delete(M, 0, axis=1)
    # M = np.delete(M, -2, axis=0)
    # M = np.delete(M, -2, axis=1)

    # K = np.delete(K, 0, axis=0)
    # K = np.delete(K, 0, axis=1)
    # K = np.delete(K, -2, axis=0)
    # K = np.delete(K, -2, axis=1)

    # Solve for eigenvalues
    eigenvalues, eigenvectors = linalg.eig(K, M)
    sorted_index = eigenvalues.argsort()
    w_squared = eigenvalues[sorted_index][2:]  # The first two natural freqs are negligible
    w = np.sqrt(w_squared)
    f = w / (2*np.pi)
    print(f)

    # mode_shapes = eigenvectors[:,sorted_index][:,2:]
    # mode_shapes /= np.max(np.abs(mode_shapes))  # Normalise mode shapes
    # p.plot_mode_shapes(mode_shapes[::2,:3], 3)

    # Damping (assumes Rayleigh damping)
    a1 = np.array([[w[0]**2, w[0]],
                   [w[1]**2, w[1]]])
    a2 = np.array([vals.zeta_1, vals.zeta_2]).reshape(2,1)
    alpha_beta = 2*(np.linalg.inv(a1) @ a2)
    C = alpha_beta[0,0]*M + alpha_beta[1,0]*K

    return M, K, C


def simulate(sim_params: dict, M: np.ndarray, K: np.ndarray, C: np.ndarray, n_free_dofs: int, plot: bool = True):

    """Calculate transient time domain response. Displacements, velocities and accelerations are calculated relative to the ground."""

    # Define initial conditions
    IC = sim_params['initial_conditions']
    # Invert mass matrix
    inverse_mass_matrix = np.linalg.inv(M)
        
    def model(t, z):

        """Second-order ODE model. Returns z_dot."""
        
        # Define the force vector
        f = np.zeros((n_free_dofs, 1))
        f[sim_params['forcing']['location'], 0] += sim_params['forcing']['signal'](t) * sim_params['forcing']['amplitude']

        # Use array slicing to extract displacement and velocity matrices returned from previous time step
        displacements = np.array([z[1::2]]).transpose()
        velocities = np.array([z[::2]]).transpose()

        # Stiffness matrix * displacement matrix
        stiffness_component = K @ displacements

        # Damping matrix * velocity matrix
        damping_component = C @ velocities

        # Calculate acceleration
        x_ddot = inverse_mass_matrix @ np.subtract(np.subtract(f, stiffness_component), damping_component)

        # Record displacement and velocity of every node
        z_dot = np.zeros(n_free_dofs*2)
        for i in range(0, n_free_dofs*2, 2):
            z_dot[i] = x_ddot[i//2, 0]
            z_dot[i+1] = z[i]

        return z_dot

    # Call solver
    result = solve_ivp(model, t_span=(0, sim_params['period']), y0=IC, method='LSODA', max_step=0.01, rtol=1e-6, atol=1e-6)
    u = result.y.T  # Transpose to get time steps in rows and DOFs in columns
    time_steps = result.t  # Time steps
    y = u[:,1::4]  # Displacements
    v = u[:,0::4]  # Velocities

    num_accelerometers = n_free_dofs//2

    # Numerically differentiating velocity to obtain acceleration
    a = np.zeros((len(time_steps), num_accelerometers))
    for i in range(len(time_steps)-1):
        for j in range(num_accelerometers):
            a[i+1,j] = ((v[i+1,j] - v[i,j])/(time_steps[i+1]-time_steps[i]))/9.81  # Convert units to g
    a = pd.DataFrame(a, columns=[f'A{i}' for i in range(num_accelerometers)])  # Accelerations
    a['t'] = time_steps

    f = [sim_params['forcing']['signal'](time) for time in a['t'].values]
    for i in range(num_accelerometers):
        a[f'F{i}'] = f

    # Interpolate to regular time grid
    new_time = np.linspace(0, sim_params['period'], sim_params['sampling_freq']*sim_params['period'])  # New time grid for interpolation
    a_interp = pd.DataFrame({'t': new_time})
    for col in ['F0', 'A0', 'F1', 'A1', 'F2', 'A2', 'F3', 'A3', 'F4', 'A4']:
        f = interp1d(a["t"], a[col], kind="cubic", fill_value="extrapolate")
        a_interp[col] = f(new_time)

    a = a_interp  # Use interpolated data

    columns = ['t', 'F0', 'A0', 'F1', 'A1', 'F2', 'A2', 'F3', 'A3', 'F4', 'A4']  # Reorder columns
    a.to_csv(f'./sim_data/{sim_params["forcing"]["type"].split(" ")[0].upper()}_{sim_params["forcing"]["location"]}.csv', index=False, columns=columns)  # Save accelerations to CSV

    if plot:
        p.plot_motion(y, v, a, time_steps, num_accelerometers)


def get_frequency_response(M, K, C, frequencies):

    """Analyse response amplitude over a range of frequencies using the FRF formula."""

    frfs = []
    for w in frequencies:
        s = complex(0, w)

        frf = np.linalg.inv(np.add(np.subtract(K, (w**2)*M), s*C))

        frfs.append(frf)

    return frfs


def solve_ode_analytically(t, m, c, k, f, ics: list):

    """Use sympy for analytical solve.""" 

    # Define function
    u = sp.Function('u')(t)

    # Define EOM LHS
    eom_lhs = m*u.diff(t, t) + c*u.diff(t) + k*u

    # Define EOM RHS
    eom_rhs = f

    # Define differential equation
    diff_eq = sp.Eq(eom_lhs, eom_rhs)

    # # Classify ode
    # print(sp.classify_ode(diff_eq))

    # Solve
    sol = sp.dsolve(diff_eq, u)
    print(sol.rhs)

    # Name constants
    # exp = sol.rhs
    # print(exp.free_symbols)
    # C2 = tuple(exp.free_symbols)[0]
    # C1 = tuple(exp.free_symbols)[2]

    # Define ICs
    ics_dict = {}
    for index, ic in enumerate(ics):
        # If even index...
        if index%2 == 0:
            ics_dict[u.diff(t).subs([(t, 0)])] = ic
        # If odd index...
        else:
            ics_dict[u.subs([(t, 0)])] = ic

    # Solve IC problem
    ivp = sp.dsolve(diff_eq, ics=ics_dict).rhs

    # # Check that solution satisfies ODE
    # print((m*ivp.diff(t, t) + c*ivp.diff(t) + k*ivp).simplify())

    return ivp, ivp.diff(t), ivp.diff(t, t)


if __name__ == '__main__':
    n_nodes = 5
    M, K, C = fe(n_nodes)

    IC = np.zeros(n_nodes*2*2)  # Number of nodes * number of DOFs at each node * 2 (displacement and velocity)
    # IC[1] = 0.001  # Displace node zero
    T = 10
    sampling_freq = 44100
    excitation_location = 0
    freq_range = np.linspace(130, 170, 10000)*2*np.pi
    frfs = get_frequency_response(M, K, C, freq_range)
    # p.plot_bode(freq_range, frfs, excitation_location)
    p.plot_nyquist(freq_range, frfs, excitation_location)
    # p.plot_im(freq_range, frfs, excitation_location)
    
    # for forcing_type in ['sine sweep']:
    #     # for location in range(3):
    #     if forcing_type == 'random':
    #         random_amplitude = np.random.random(len(freq_range)) + 1
    #         random_phase = np.random.uniform(-np.pi, np.pi, len(freq_range))
    #         forcing_fnc = lambda t: sum([np.sin(freq*t + phi) * amp for freq, phi, amp in zip(freq_range, random_phase, random_amplitude)])
    #     elif forcing_type == 'stepped sweep':
    #         signal_time = 4/(np.min(freq_range)/(2*np.pi))  # 4 periods per frequency
    #         T = signal_time*len(freq_range)
    #         forcing_fnc = lambda t: np.sin(t*freq_range[int(t//signal_time)]) if (t % signal_time) < signal_time else 0
    #     elif forcing_type == 'sine':
    #         freq = 20
    #         forcing_fnc = lambda t: np.sin(2*np.pi*freq*t)
    #     elif forcing_type == 'sine sweep':
    #         freq_low = 10
    #         freq_high = 1000
    #         hz_per_second = (freq_high - freq_low) / T
    #         forcing_fnc = lambda t: np.sin(2*np.pi*(freq_low+(hz_per_second*t))*t)

    #     time_steps = np.linspace(0, T, int(T*sampling_freq))
    #     force = forcing_fnc(time_steps)
    #     plt.plot(time_steps, force)
    #     plt.title('Forcing Function')
    #     plt.show()

    #     sim_params = {
    #         'period': T,
    #         'initial_conditions': IC,
    #         'sampling_freq': sampling_freq,
    #         'forcing': {
    #             'location': excitation_location,
    #             'amplitude': 1,
    #             'signal': forcing_fnc,
    #             'type': forcing_type
    #         }
    #     }
    #     simulate(sim_params, M, K, C, n_free_dofs=10, plot=True)