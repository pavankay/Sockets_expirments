const socket = io();
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const colorInfo = document.getElementById('colorInfo');

const PLAYER_SIZE = 50;
const MOVE_SPEED = 5;

let myColor;
let myId;
let positions = {};
let keys = {};

function resizeCanvas() {
    canvas.width = window.innerWidth - 20;
    canvas.height = window.innerHeight - 20;
    drawGameState();
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

socket.on('init', (data) => {
    myColor = data.color;
    myId = data.id;
    colorInfo.textContent = `You are: ${myColor}`;
});

socket.on('update_positions', (newPositions) => {
    positions = newPositions;
    drawGameState();
});

function drawGameState() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let id in positions) {
        const pos = positions[id];
        ctx.fillStyle = pos.color;
        ctx.fillRect(pos.x, pos.y, PLAYER_SIZE, PLAYER_SIZE);
    }
}

function updatePosition() {
    if (!myId || !positions[myId]) return;

    let dx = 0;
    let dy = 0;

    if (keys['ArrowLeft']) dx -= MOVE_SPEED;
    if (keys['ArrowRight']) dx += MOVE_SPEED;
    if (keys['ArrowUp']) dy -= MOVE_SPEED;
    if (keys['ArrowDown']) dy += MOVE_SPEED;

    if (dx !== 0 || dy !== 0) {
        socket.emit('move', { x: dx, y: dy });
    }
}

document.addEventListener('keydown', (event) => {
    keys[event.key] = true;
    event.preventDefault();
});

document.addEventListener('keyup', (event) => {
    keys[event.key] = false;
});

setInterval(() => {
    updatePosition();
}, 1000 / 60);  // 60 FPS

drawGameState();
drawGameState();