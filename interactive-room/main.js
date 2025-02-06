// Set up the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 2); // Ambient light
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 3, 100); // Point light
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// Orbit controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Load the room model
const loader = new THREE.GLTFLoader();
let room; // Store the loaded room model

loader.load('/interactive-room/room.glb', (gltf) => {
    console.log("Model Loaded Successfully!", gltf.scene);
    room = gltf.scene;
    scene.add(room);

    // Find monitor and door objects by name
    const monitor = room.getObjectByName('monitor');
    const door = room.getObjectByName('door');

    if (monitor && door) {
        console.log('Monitor and door found!');
    } else {
        console.error('Monitor or door not found. Check object names in Blender.');
    }
}, undefined, (error) => {
    console.error("Error loading model:", error);
});

// Position the camera
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

// Set up raycaster and mouse variables
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let highlightedObject = null;

// Mouse movement event
window.addEventListener('mousemove', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        const object = intersects[0].object;
        if (object.name === 'monitor' || object.name === 'door') {
            highlightObject(object);
        } else {
            removeHighlight();
        }
    } else {
        removeHighlight();
    }
});

// Mouse click event
window.addEventListener('click', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        const object = intersects[0].object;
        if (object.name === 'monitor') {
            alert('You clicked the monitor!');
        } else if (object.name === 'door') {
            alert('You clicked the door!');
        }
    }
});

// Highlight function
function highlightObject(object) {
    if (highlightedObject !== object) {
        removeHighlight();
        object.originalMaterial = object.material;
        object.material = new THREE.MeshBasicMaterial({ color: 0xff0000 }); // Red highlight
        highlightedObject = object;
    }
}

// Remove highlight function
function removeHighlight() {
    if (highlightedObject) {
        highlightedObject.material = highlightedObject.originalMaterial;
        highlightedObject = null;
    }
}

// Render loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();
