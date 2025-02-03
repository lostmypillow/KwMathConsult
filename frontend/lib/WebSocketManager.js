class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.isConnected = false;
    }

    connect(onMessage, onError, onClose) {
        if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
            this.socket = new WebSocket(this.url);

            this.socket.onopen = () => {
                this.isConnected = true;
                console.log("WebSocket connection established.");
            };

            this.socket.onmessage = (event) => {
                if (onMessage) {
                    try {
                        onMessage(event.data)
                    } catch (error) {
                        console.error("Error parsing WebSocket message:", error);
                    }
                }
            };

            this.socket.onerror = (error) => {
                this.isConnected = false;
                if (onError) onError(error);
                console.error("WebSocket error:", error);
            };

            this.socket.onclose = () => {
                this.isConnected = false;
                if (onClose) onClose();
                console.log("WebSocket connection closed.");
            };
        }
    }

    disconnect() {
        if (this.socket && this.socket.readyState !== WebSocket.CLOSED) {
            this.socket.close();
        }
    }
}

export default WebSocketManager;