// static/webrtc.js

const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

let pc;

navigator.mediaDevices
  .getUserMedia({ video: true, audio: true })
  .then((stream) => {
    localVideo.srcObject = stream;

    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => {
      pc = createPeerConnection();
      pc.addStream(stream);
      pc.createOffer()
        .then((offer) => pc.setLocalDescription(offer))
        .then(() => {
          ws.send(
            JSON.stringify({ type: "video-offer", data: pc.localDescription })
          );
        })
        .catch((error) => console.error("Error creating offer:", error));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "video-answer") {
        pc.setRemoteDescription(new RTCSessionDescription(data.data));
      }
    };
  })
  .catch((error) => console.error("Error accessing media devices:", error));

function createPeerConnection() {
  const configuration = {
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
  };
  const pc = new RTCPeerConnection(configuration);

  // Assuming you have defined your on_ice_candidate, on_negotiation_needed, etc. event handlers here

  return pc;
}
