# 🤖 Chatbot API Client

A JavaScript/TypeScript client for seamless interaction with the Chatbot server, now supporting API key authentication.

---

## 📥 Installation

### 📍 Local Development (npm link)

Use during local development:

```bash
npm run build
npm link

# In your project directory
npm link @schmitech/chatbot-api
```

### 📂 Local Directory Install

Direct local installation:

```bash
npm run build
npm install /path/to/qa-chatbot-server/api
```

### 🌐 CDN Integration

Integrate directly into websites via CDN:

```html
<script type="module">
  import { configureApi, streamChat } from 'https://cdn.jsdelivr.net/npm/@schmitech/chatbot-api/dist/api.mjs';

  configureApi({
    apiUrl: 'https://your-api-server.com',
    apiKey: 'your-api-key'
  });

  async function handleChat() {
    for await (const response of streamChat('Hello', false)) {
      console.log(response.text);
    }
  }
</script>
```

---

## ⚙️ Usage

### 🚨 Configuration (Required)

You must configure the API client before usage:

```javascript
import { configureApi, streamChat } from '@schmitech/chatbot-api';

configureApi({
  apiUrl: 'https://your-api-server.com',
  apiKey: 'your-api-key'
});
```

### 📖 Basic Example

```javascript
async function chat() {
  configureApi({ apiUrl: 'https://your-api-server.com', apiKey: 'your-api-key' });

  for await (const response of streamChat('Hello, how can I help?', false)) {
    console.log(response.text);
    if (response.done) console.log('Chat complete!');
  }
}

chat();
```

### 🎙️ Voice-enabled Example

```javascript
async function chatWithVoice() {
  configureApi({ apiUrl: 'https://your-api-server.com', apiKey: 'your-api-key' });

  for await (const response of streamChat('Tell me a joke', true)) {
    if (response.type === 'audio') {
      console.log('Received audio content');
    } else {
      console.log(response.text);
    }
    if (response.done) console.log('Chat complete!');
  }
}

chatWithVoice();
```

---

## ⚛️ React Integration

Configure once globally:

```jsx
import React, { useState } from 'react';
import { configureApi, streamChat } from '@schmitech/chatbot-api';

configureApi({
  apiUrl: 'https://your-api-server.com',
  apiKey: 'your-api-key'
});

function ChatComponent() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessages(prev => [...prev, { text: input, isUser: true }]);

    let responseText = '';
    for await (const response of streamChat(input, false)) {
      responseText += response.text;
      setMessages(prev => [...prev, { text: responseText, isUser: false }]);
      if (response.done) break;
    }
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button type="submit">Send</button>
    </form>
  );
}

export default ChatComponent;
```

---

## 📱 Mobile Usage

### 📲 React Native

```javascript
configureApi({ apiUrl: 'https://your-api-server.com', apiKey: 'your-api-key' });

async function handleChat(message) {
  for await (const response of streamChat(message, false)) {
    // Handle response
  }
}
```

---

## 📚 API Reference

### `configureApi(config)`

| Parameter | Description | Required |
|-----------|-------------|----------|
| `apiUrl`  | Chatbot API URL | ✅ Yes |
| `apiKey`  | API key for authentication | ✅ Yes |

### `streamChat(message, voiceEnabled)`

Streams responses from the server:
- `message`: Message string
- `voiceEnabled`: Boolean, enables audio response

Returns an async generator yielding:
```typescript
interface StreamResponse {
  text?: string;
  content?: string;
  done?: boolean;
  type?: string;
}
```

---

## 🛠️ Development

### 🧪 Testing

```bash
npm run build
npm test
npm run test:watch
npm run test-query "your query" "http://your-api-server.com" "your-api-key"
```

---

## 📃 License

MIT License - See [LICENSE](LICENSE).