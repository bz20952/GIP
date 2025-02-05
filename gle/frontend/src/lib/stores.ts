import { writable } from 'svelte/store';

export const splash = writable(true);

export const showResultsForm = writable([]);

export const showFeedback = writable([]);

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

export const progress = writable({
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