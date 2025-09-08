import React from 'react';
import {
  Box,
  TextField,
  Button,
  Stack,
} from '@mui/material';
import { ChatInputProps } from '../types/chat';

const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChange,
  onSubmit,
  isLoading
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim() || isLoading) return;
    onSubmit(value.trim());
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
      <form onSubmit={handleSubmit}>
        <Stack direction="row" spacing={1}>
          <TextField
            fullWidth
            value={value}
            onChange={handleChange}
            placeholder="Type your message..."
            disabled={isLoading}
            size="small"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!value.trim() || isLoading}
            sx={{ minWidth: 80 }}
          >
            Send
          </Button>
        </Stack>
      </form>
    </Box>
  );
};

export default ChatInput;
