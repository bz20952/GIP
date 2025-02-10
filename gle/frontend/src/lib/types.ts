
/////////////////////////////////////////////////////////////////////////////

export interface Result {
    name: string;
    unit: string;
    answer: number;
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
    feedback: Feedback[];
}

/////////////////////////////////////////////////////////////////////////////

export interface Task {
    emailId: number;
    answers: any[];
    feedbackStage: number;
}

export interface Progress {
    total: number;
    current: number;
    tasks: Task[];
}

/////////////////////////////////////////////////////////////////////////////

export interface Tool {
    name: string;
    available: boolean;
    type: string;
    description: string;
}