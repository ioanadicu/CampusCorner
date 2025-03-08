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
controls.target.set(0, 0, 0);  // Ensure the target is the center of the scene (room's center)
controls.update();  // Update controls to reflect the change


// Set zoom limits
controls.minDistance = 8;  // Minimum zoom-in
controls.maxDistance = 30; // Maximum zoom-out

// Prevent camera from going below floor level
controls.addEventListener('change', () => {
    if (camera.position.y < 1) { // Floor level at y = 1
        camera.position.y = 1;
    }
});


// Load the room model
const loader = new THREE.GLTFLoader();
let room; // Store the loaded room model


loader.load("/static/Bedroom102.glb", (gltf) => {
    console.log("Model Loaded Successfully!", gltf.scene);
    room = gltf.scene;
    scene.add(room);

    // Traverse the loaded scene and log all object names
    room.traverse((child) => {
        if (child.isMesh) {
            console.log("Object name:", child.name);
        }
    });

    // Find monitor, door, and calendar objects by name
    const monitor = room.getObjectByName('Monitor');
    const door = room.getObjectByName('Door');
    const calendar = room.getObjectByName('Calendar');
    if (monitor) console.log('Monitor found!');
    if (door) console.log('Door found!');
    if (calendar) console.log('Calendar found!');

    if (!monitor || !door || !calendar) {
        console.error('One or more objects not found. Check object names in Blender.');
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

// Set up EffectComposer for post-processing
const composer = new THREE.EffectComposer(renderer);
const renderPass = new THREE.RenderPass(scene, camera);
composer.addPass(renderPass);

// Set up OutlinePass
const outlinePass = new THREE.OutlinePass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    scene,
    camera
);
outlinePass.edgeStrength = 5.0;
outlinePass.edgeGlow = 0.0;
outlinePass.edgeThickness = 3.0;
outlinePass.pulsePeriod = 2;
outlinePass.visibleEdgeColor.set(0xffff99);
outlinePass.hiddenEdgeColor.set(0xffff99);


composer.addPass(outlinePass);

// To dynamically highlight objects
let selectedObjects = [];

function setHighlightedObject(object) {
    selectedObjects = object ? [object] : [];
    outlinePass.selectedObjects = selectedObjects;
}

// Mouse move event for hover highlighting


// Render loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    composer.render(); // Use composer for post-processing
}
animate();