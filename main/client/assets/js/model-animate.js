// radhe radhe
const canvas = document.querySelector('.chess-board-bg');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.position.set(5, 5, 5);
    camera.lookAt(0, 0, 0);
    
    const pointLight = new THREE.PointLight(0xffffff, 2, 100);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);
    
    const controls = (function() {
        const _this = {};
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };
        let spherical = {
            radius: Math.sqrt(camera.position.x ** 2 + camera.position.y ** 2 + camera.position.z ** 2),
            theta: Math.atan2(camera.position.x, camera.position.z),
            phi: Math.acos(camera.position.y / Math.sqrt(camera.position.x ** 2 + camera.position.y ** 2 + camera.position.z ** 2))
        };
        
        canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            previousMousePosition = { x: e.clientX, y: e.clientY };
        });
        
        canvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const deltaX = e.clientX - previousMousePosition.x;
                const deltaY = e.clientY - previousMousePosition.y;
                
                spherical.theta -= deltaX * 0.005;
                spherical.phi -= deltaY * 0.005;
                spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));
                
                camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
                camera.position.y = spherical.radius * Math.cos(spherical.phi);
                camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
                camera.lookAt(0, 0, 0);
                
                previousMousePosition = { x: e.clientX, y: e.clientY };
            }
        });
        
        canvas.addEventListener('mouseup', () => { isDragging = false; });
        canvas.addEventListener('mouseleave', () => { isDragging = false; });
        
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            spherical.radius += e.deltaY * 0.01;
            spherical.radius = Math.max(1, Math.min(50, spherical.radius));
            
            camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.position.y = spherical.radius * Math.cos(spherical.phi);
            camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.lookAt(0, 0, 0);
        });
        
        return _this;
    })();
    
    const loader = new THREE.GLTFLoader();
    const glbUrl = 'http://127.0.0.1:3000/test/client/assets/models/chess_board.glb';
    
    let chessBoard;
    loader.load(glbUrl, function(gltf) {
        chessBoard = gltf.scene;
        scene.add(chessBoard);
    });
    
    function animate() {
        requestAnimationFrame(animate);
        if (chessBoard) {
            chessBoard.rotation.y += 0.005;
        }
        renderer.render(scene, camera);
    }
    
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    animate();