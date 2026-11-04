import React, { useEffect, useRef, useState } from "react";

export default function App() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [status, setStatus] = useState("Disconnected");
  const wsRef = useRef<WebSocket | null>(null);

  const startLightboard = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setIsStreaming(true);
      setStatus("Connecting to Colab Vision Backend...");

      // Connect to your live Google Colab Ngrok WebSocket URL
      const ws = new WebSocket("wss://babied-krypton-staging.ngrok-free.dev/ws/vision");
      wsRef.current = ws;

      ws.onopen = () => {
        setStatus("Connected (Live YOLOv11-Pose Active)");
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        // Clear canvas and draw cursor/drawing feedback
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw index fingertip cursor
        ctx.beginPath();
        ctx.arc(data.x, data.y, 8, 0, 2 * Math.PI);
        ctx.fillStyle = data.isDrawing ? "#ef4444" : "#3b82f6";
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
      };

      ws.onclose = () => {
        setStatus("Disconnected from backend.");
      };

      // Stream frames every 50ms (20 FPS)
      setInterval(() => {
        if (ws.readyState === WebSocket.OPEN && videoRef.current && canvasRef.current) {
          const video = videoRef.current;
          const canvas = canvasRef.current;
          canvas.width = video.videoWidth || 640;
          canvas.height = video.videoHeight || 480;
          const ctx = canvas.getContext("2d");
          if (!ctx) return;

          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          canvas.toBlob(
            (blob) => {
              if (blob && ws.readyState === WebSocket.OPEN) {
                ws.send(blob);
              }
            },
            "image/jpeg",
            0.6
          );
        }
      }, 50);

    } catch (err) {
      console.error("Webcam error:", err);
      setStatus("Webcam permission denied.");
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-white">
      <div className="max-w-4xl w-full rounded-2xl border border-slate-700 bg-slate-900 p-6 text-center shadow-2xl">
        <h1 className="text-3xl font-bold mb-2">OmniPhysics Lightboard Studio</h1>
        <p className="text-slate-400 mb-4">Status: <span className="text-green-400 font-semibold">{status}</span></p>

        <div className="relative inline-block w-[640px] h-[480px] bg-black rounded-lg overflow-hidden border border-slate-700">
          <video ref={videoRef} className="absolute inset-0 w-full h-full object-cover -scale-x-100" muted playsInline />
          <canvas ref={canvasRef} className="absolute inset-0 w-full h-full object-cover -scale-x-100 pointer-events-none" />
        </div>

        <div className="mt-6">
          {!isStreaming ? (
            <button
              onClick={startLightboard}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 transition"
            >
              Activate Lightboard
            </button>
          ) : (
            <p className="text-sm text-blue-400">Lightboard Active & Streaming to Cloud Backend 🚀</p>
          )}
        </div>
      </div>
    </main>
  );
}