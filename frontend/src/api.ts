const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface ReplyRequest {
    message: string;
    lead?: Record<string, any>;
    community_id?: string;
}

export interface MessageContent {
    role: "user" | "assistant";
    content: string;
}

export interface MessageData {
    id: string;  // UUID from backend
    message: MessageContent;
    created_date: string;
}

export type ActionType = "propose_tour" | "ask_clarification" | "handoff_human";

// New simplified response structure
export interface ApiResponse {
    id: string;  // UUID we generate
    reply: string;  // The content the agent replies back with
    created_date: string;  // The create time of this reply
    action: ActionType;  // Default to ask_clarification
    propose_time?: string;  // Only present when we want to propose a tour booking
}

export const postReply = async (message: string, lead?: Record<string, any>): Promise<ApiResponse> => {
    const payload: ReplyRequest = {
        message,
        community_id: "sunset-ridge" // Default community for now
    };
    if (lead) {
        payload.lead = lead;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/reply`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: ApiResponse = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to get response from server');
    }
};

export const getMessages = async (limit: number = 100) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages?limit=${limit}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to fetch messages');
    }
};
