export interface Message {
    id: string;  // UUID from backend
    message: {
        role: "user" | "assistant";
        content: string;
    };
    created_date: string;
    action?: "propose_tour" | "ask_clarification" | "handoff_human";
    propose_time?: string;
}

export interface ChatInputProps {
    value: string;
    onChange: (value: string) => void;
    onSubmit: (message: string) => void;
    isLoading: boolean;
}

export interface MessageItemProps {
    message: Message;
}

export interface MessageListProps {
    messages: Message[];
}

export interface ChatHeaderProps {
    title?: string;
    subtitle?: string;
}
