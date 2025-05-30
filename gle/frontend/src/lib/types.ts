
/////////////////////////////////////////////////////////////////////////////

export interface Result {
    subtaskId: number;
    name: string;
    inputType: string;
    options: Array<string>;
    unit: string;
    tooltipId: number;
    answer: number | Object | string;
    praise: string;
    feedback: Feedback[];
}

export interface Feedback {
    stage: number;
    message: string;
}

export interface Email {
    id: number;
    sender: string;
    subject: string;
    body: string;
    results: Result[];
    unlocks: string[];
}

/////////////////////////////////////////////////////////////////////////////

export interface Progress {
    total: number;
    current: number;
    currentTask: Task;
    displayMessage: DisplayMessage[];
}

export interface Task {
    emailId: number;
    currentSubtask: Subtask;
}

export interface Subtask {
    subtaskId: number;
    answer: any;
    feedbackStage: number;
    attempts: number;
    correct: boolean;
}

export interface DisplayMessage {
    emailId: number;
    message: string;
    colour: string;
}

/////////////////////////////////////////////////////////////////////////////

export interface Tool {
    name: string;
    available: boolean;
    type: string;
    description: string;
    endpoint?: string;
}

/////////////////////////////////////////////////////////////////////////////

export interface TestOptions {
    serialNumber: string | undefined;
    accelerometers: {
        A0: boolean;
        A1: boolean;
        A2: boolean;
        A3: boolean;
        A4: boolean;
    };
    shakerPosition: number;
    excitationType: string;
    tipHardness: string;
    samplingFreq: number;
    filterType: string;
    lowerCutoff: number;
    upperCutoff: number;
}