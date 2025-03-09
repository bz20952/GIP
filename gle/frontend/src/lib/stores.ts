import { writable, type Writable } from 'svelte/store';
import type { Tool, Progress } from './types';

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
        description: 'Tap a beam with a hammer and record the applied force and acceleration. Typically used to determine natural frequencies and frequency response.'
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
        available: true,
        type: 'signalProcessing',
        description: 'A mathematical tool used to convert discrete time-domain data to the frequency-domain.'
    },
    {
        name: 'Bode',
        available: false,
        type: 'signalProcessing',
        description: 'Visualise the gain and phase of the frequency response. May be used to estimate natural frequencies and modal damping ratios.'
    },
    {
        name: 'Nyquist',
        available: false,
        type: 'signalProcessing',
        description: 'Visualise the gain and phase of the frequency response. May be used to estimate natural frequencies and modal damping ratios.'
    },
    {
        name: 'Frequency response function',
        available: false,
        type: 'analysis',
        description: 'Visualise the gain and phase of the frequency response across a range of forcing frequencies. May be used to estimate natural frequencies and modal damping ratios.'
    },
    {
        name: 'Circle fitting',
        available: false,
        type: 'analysis',
        description: 'Use the Nyquist plot to estimate modal damping ratios.'
    },
    {
        name: 'Half power',
        available: false,
        type: 'analysis',
        description: 'Use the Bode plot to estimate modal damping ratios.'
    }
]);

export const progress: Writable<Progress> = writable({
    total: 5,
    current: 0,
    tasks: [
        {
            emailId: 1,
            answers: [],
            feedbackStage: 0,
        },
        {
            emailId: 2,
            answers: [],
            feedbackStage: 0,
        },
        {
            emailId: 3,
            answers: [],
            feedbackStage: 0,
        },
        {
            emailId: 4,
            answers: [],
            feedbackStage: 0,
        },
        {
            emailId: 5,
            answers: [],
            feedbackStage: 0,
        },
    ]
});

export const testOptions: Writable<any> = writable({
    "sessionId": Math.random().toString(36).substring(2, 14),
    "accelerometers": {
        "A0": true,
        "A1": false,
        "A2": false,    
        "A3": false,
        "A4": false
    },
    "shakerPosition": "l/2",
    "excitationType": "Free vibration",
    "samplingFreq": 512,
    "filterType": "lowPass",
    "lowerCutoff": 0,
    "upperCutoff": 0
});