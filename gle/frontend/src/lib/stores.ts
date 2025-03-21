import { writable, type Writable } from 'svelte/store';
import type { Tool, Progress, TestOptions } from './types';
import { emails } from '$lib/emails.json';

export const splash: Writable<boolean> = writable(true);

export const showResultsForm: Writable<number[]> = writable([]);

export const showFeedback: Writable<number[]> = writable([]);

export const tools: Writable<Tool[]> = writable([
    {
        name: 'Free vibration',
        available: true,
        type: 'excitation',
        description: 'Displace and release a beam with no external forcing. Typically used to determine the fundamental natural frequency.'
    },
    {
        name: 'Random excitation',
        available: true,
        type: 'excitation',
        description: 'Generate a random signal which is passed to a shaker and used to excite a beam. Typically used to simulate real-world excitation.'
    },
    {
        name: 'Hammer testing',
        available: false,
        type: 'excitation',
        description: 'Tap a beam with a hammer and record the applied force and acceleration. Typically used as a quick test to obtain natural frequencies.'
    },
    {
        name: 'Sine sweep',
        available: false,
        type: 'excitation',
        description: 'Generate a sine wave signal which gradually changes frequency. Typically used to search for resonance.'
    },
    {
        name: 'Stepped sweep',
        available: false,
        type: 'excitation',
        description: 'Generate a stepped signal which gradually changes frequency. Typically used to determine natural frequencies.'
    },
    {
        name: 'Discrete Fourier transform',
        available: false,
        type: 'analysis',
        description: 'A mathematical tool used to convert discrete time-domain data to the frequency-domain.',
        endpoint: 'dft'
    },
    {
        name: 'Bode',
        available: false,
        type: 'identification',
        description: 'Visualise the gain and phase of the frequency response. May be used to estimate natural frequencies and modal damping ratios.',
        endpoint: 'bode'
    },
    {
        name: 'Nyquist',
        available: false,
        type: 'identification',
        description: 'Visualise the gain and phase of the frequency response. May be used to estimate natural frequencies and modal damping ratios.',
        endpoint: 'nyquist'
    },
    {
        name: 'Mode shapes',
        available: false,
        type: 'identification',
        description: 'Visualise the mode shape from the frequency response.',
        endpoint: 'mode-shapes'
    }
    // {
    //     name: 'Frequency response function',
    //     available: false,
    //     type: 'analysis',
    //     description: 'Visualise the gain and phase of the frequency response across a range of forcing frequencies. May be used to estimate natural frequencies and modal damping ratios.'
    // },
    // {
    //     name: 'Circle fitting',
    //     available: false,
    //     type: 'analysis',
    //     description: 'Use the Nyquist plot to estimate modal damping ratios.'
    // },
    // {
    //     name: 'Half power',
    //     available: false,
    //     type: 'analysis',
    //     description: 'Use the Bode plot to estimate modal damping ratios.'
    // }
]);

export const progress: Writable<Progress> = writable({
    total: emails.length,
    current: 0,
    currentTask: {
        emailId: 1,
        currentSubtask: {
            subtaskId: 1,
            answer: undefined,
            feedbackStage: 0,
            attempts: 0,
            correct: false
        }
    },
    displayMessage: emails.map(email => ({ emailId: email.id, message: 'There is no feedback yet for this task.', colour: '#333' }))
});

export const testOptions: Writable<TestOptions> = writable({
    "serialNumber": undefined,
    "accelerometers": {
        "A0": true,
        "A1": false,
        "A2": false,    
        "A3": false,
        "A4": false
    },
    "shakerPosition": 2,
    "excitationType": "Free vibration",
    "tipHardness": "Soft",
    "samplingFreq": 512,
    "filterType": "none",
    "lowerCutoff": 0,
    "upperCutoff": 0
});