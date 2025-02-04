import { writable } from 'svelte/store';

export const splash = writable(true);

export const resultsForm = writable(false);

export const feedback = writable(false);

export const tools = writable([
    {
        name: 'Free vibration',
        available: true,
        type: 'excitation',
    },
    {
        name: 'Random excitation',
        available: true,
        type: 'excitation',
    },
    {
        name: 'Hammer testing',
        available: false,
        type: 'excitation',
    },
    {
        name: 'Sine sweep',
        available: false,
        type: 'excitation',
    },
    {
        name: 'Stepped sweep',
        available: false,
        type: 'excitation',
    },
    {
        name: 'Discrete Fourier transform',
        available: true,
        type: 'signalProcessing',
    },
    {
        name: 'Circle fitting',
        available: false,
        type: 'analysis',
    },
    {
        name: 'Half power',
        availability: true,
        type: 'analysis',
    }
]);

