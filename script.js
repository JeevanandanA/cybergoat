// Mobile Menu Toggle
const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');

if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active') && !menuBtn.contains(e.target) && !navLinks.contains(e.target)) {
            toggleMenu();
        }
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) toggleMenu();
        });
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 992 && navLinks.classList.contains('active')) toggleMenu();
    });
}

const formStatus = document.querySelector('#formStatus');
if (formStatus && new URLSearchParams(window.location.search).get('sent') === '1') {
    formStatus.hidden = false;
}

// Function to toggle menu
function toggleMenu() {
    menuBtn.classList.toggle('active');
    navLinks.classList.toggle('active');
    
    // Prevent body scroll when menu is open
    if (navLinks.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const selector = this.getAttribute('href');
        if (!selector || selector === '#') {
            e.preventDefault();
            return;
        }
        const target = document.querySelector(selector);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
const sceneCanvas = document.createElement('canvas');
sceneCanvas.className = 'scene-canvas';
document.body.prepend(sceneCanvas);
const sceneContext = sceneCanvas.getContext('2d');
const scenePoints = [];
const pointer = { x: 0, y: 0 };
let sceneWidth = 0;
let sceneHeight = 0;

function resizeScene() {
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    sceneWidth = window.innerWidth;
    sceneHeight = window.innerHeight;
    sceneCanvas.width = sceneWidth * pixelRatio;
    sceneCanvas.height = sceneHeight * pixelRatio;
    sceneContext.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
}

function seedScene() {
    scenePoints.length = 0;
    for (let index = 0; index < 42; index += 1) {
        scenePoints.push({ x: Math.random() * 2 - 1, y: Math.random() * 2 - 1, z: Math.random() * 2 + .2, phase: Math.random() * Math.PI * 2 });
    }
}

function drawScene(time) {
    sceneContext.clearRect(0, 0, sceneWidth, sceneHeight);
    const projected = scenePoints.map(point => {
        point.z -= .00035;
        if (point.z < .2) point.z = 2.2;
        const scale = 230 / point.z;
        return { x: sceneWidth / 2 + point.x * scale + pointer.x * 18, y: sceneHeight / 2 + point.y * scale + pointer.y * 12, size: Math.max(1, 3 / point.z) };
    });
    sceneContext.lineWidth = 1;
    projected.forEach((point, index) => {
        projected.slice(index + 1).forEach(other => {
            const distance = Math.hypot(point.x - other.x, point.y - other.y);
            if (distance < 115) {
                sceneContext.strokeStyle = `rgba(145, 230, 61, ${Math.max(0, .17 - distance / 900)})`;
                sceneContext.beginPath(); sceneContext.moveTo(point.x, point.y); sceneContext.lineTo(other.x, other.y); sceneContext.stroke();
            }
        });
        sceneContext.fillStyle = 'rgba(145, 230, 61, .65)';
        sceneContext.beginPath(); sceneContext.arc(point.x, point.y, point.size, 0, Math.PI * 2); sceneContext.fill();
    });
    requestAnimationFrame(drawScene);
}

resizeScene();
seedScene();
window.addEventListener('resize', resizeScene);
window.addEventListener('pointermove', event => { pointer.x = event.clientX / sceneWidth - .5; pointer.y = event.clientY / sceneHeight - .5; });
requestAnimationFrame(drawScene);
}