# OmniPhysics — Steering & Architecture Guidelines

## Project Concept
Interactive 3D physics education platform combining in-browser MediaPipe hand tracking for zero-latency 3D mid-air drawing, Three.js simulation visualizers, and a context-aware AI physics tutor.

## Core Directives
1. Low-Latency Vision: Hand landmark tracking must run client-side using WebAssembly / Web Workers (MediaPipe Hands). No frame data should be sent over the network.
2. Architecture:
   - frontend/: React + Vite + Three.js / React Three Fiber + Tailwind CSS.
   - backend/: FastAPI + Python for physics Q&A streaming (SSE) and problem solving.
   - .kiro/: Maintained at repo root for specs, steering, and agent hooks.
3. Separation of Work:
   - Waseem Abbas: Vision pipeline, raycasting to 3D world space, CI/CD, system security.
   - Arsalan Iqbal: UI/UX design system (Figma), React HUD components, Three.js 3D model scenes.
   - Tofeeque Rahman: FastAPI backend, streaming LLM integration, LaTeX equation handling.
