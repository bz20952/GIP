import { writable, type Writable } from 'svelte/store';
import type { Tool, Progress, Task } from './types';

export const splash: Writable<boolean> = writable(true);

export const showResultsForm: Writable<number[]> = writable([]);

export const showFeedback: Writable<number[]> = writable([]);

export const tools: Writable<Tool[]> = writable([
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
        name: 'Bode',
        available: false,
        type: 'signalProcessing',
    },
    {
        name: 'Nyquist',
        available: false,
        type: 'signalProcessing',
    },
    {
        name: 'Frequency response function',
        available: false,
        type: 'analysis'
    },
    {
        name: 'Circle fitting',
        available: false,
        type: 'analysis',
    },
    {
        name: 'Half power',
        available: false,
        type: 'analysis',
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