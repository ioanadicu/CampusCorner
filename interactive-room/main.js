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

loader.load('./room7.glb', (gltf) => {
    console.log("Model Loaded Successfully!", gltf.scene);
    room = gltf.scene;
    scene.add(room);

    // Traverse the loaded scene and log all object names
    room.traverse((child) => {
        if (child.isMesh) {
            console.log("Object name:", child.name);
        }
    });

    // Find monitor and door objects by name
    const monitor = room.getObjectByName('Monitor');
    const door = room.getObjectByName('Door');
    const bed = room.getObjectByName('Bed')

    if (monitor) {
        console.log('Monitor found!');
    } 
    if (door) {
        console.log("Door found")
    }
    if (bed) {
        console.log("Bed found")
    }
    else {
        console.error('Monitor or door or Bed not found. Check object names in Blender.');
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
outlinePass.edgeStrength = 3.0;
outlinePass.edgeGlow = 0.0;
outlinePass.edgeThickness = 1.0;
outlinePass.pulsePeriod = 0;
outlinePass.visibleEdgeColor.set(0xffff99);
outlinePass.hiddenEdgeColor.set(0x000000);
composer.addPass(outlinePass);

// To dynamically highlight objects
let selectedObjects = [];

function addSelectedObject(object) {
    selectedObjects = [object];
    outlinePass.selectedObjects = selectedObjects;
}

function clearSelectedObjects() {
    selectedObjects = [];
    outlinePass.selectedObjects = [];
}

// Mouse move event
window.addEventListener('mousemove', (event) => {
    // Calculate mouse position
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Update raycaster
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    const tooltip = document.getElementById('tooltip');
    if (intersects.length > 0) {
        let object = intersects[0].object;

        // Traverse up the hierarchy to find a meaningful parent name
        while (object.parent && object.parent.type !== 'Scene') {
            if (object.name) break; // Stop if the object has a name
            object = object.parent;
        }

        // Display tooltip for any object with a name
        if (object.name) {
            tooltip.style.display = 'block';
            tooltip.style.left = event.clientX + 10 + 'px'; // Offset from mouse
            tooltip.style.top = event.clientY + 10 + 'px';
            tooltip.textContent = object.name; // Show object's name
        } else {
            tooltip.style.display = 'none'; // Hide tooltip if no meaningful name
        }
    } else {
        tooltip.style.display = 'none'; // Hide tooltip if no object is hovered
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

        if (object.name === 'Monitor') {
            console.log('You clicked the monitor!');
            addSelectedObject(object);
        } else if (object.name === 'Door') {
            console.log('You clicked the door!');
            addSelectedObject(object);
        }
        else if (object.name === 'Calendar') {
            console.log('You clicked the Calendar!');
            addSelectedObject(object); // 
        }
        else if (object.name === 'Bed') {
            console.log('You clicked the Bed!');
            addSelectedObject(object); // 
        }
        else {
        clearSelectedObjects();
    }
}});

// Render loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    composer.render(); // Use composer for post-processing
}
animate();
