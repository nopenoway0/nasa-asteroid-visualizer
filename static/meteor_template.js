async function init() {

	container = document.getElementById( 'container' );

	//

	camera = new THREE.PerspectiveCamera( 27, window.innerWidth / window.innerHeight, 5, 1000000000 );
	camera.position.z = 5000;

	var light = new THREE.PointLight( 0xff0000, 1, 100 );

	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0x050505 );
	//scene.fog = new THREE.Fog( 0x050505, 2000, 3500 );
	scene.add(light)
	controls = new THREE.OrbitControls( camera );
	controls.enablePan = false;
	var particles = meteors.length;

	var geometry = new THREE.BufferGeometry();

	var positions = [];
	var colors = [];
	var sizes = []
	var color = new THREE.Color();

	var radius = 650
	var n = 1000, n2 = n / 2; // particles spread in the cube

	for ( var i = 0; i < particles; i ++ ) {



		// positions
		//var x = (Math.random() - .5)
		//var y = (Math.random() - .5)
		//var z = (Math.random() - .5)
		//var magnitude = Math.sqrt(x*x + y*y + z*z)
		//x /= magnitude
		//y /= magnitude
		//z /= magnitude
		//positions.push( x * radius * Math.random() , y * radius * Math.random(), z * radius * Math.random());
		//colors.push(0, 0, 0)
		positions.push(meteors[i].miss_distance.amount / 100 * -1, 0, 0)
	}

	geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) );

	geometry.computeBoundingSphere();

	// create asteroids
	var texture =  new THREE.TextureLoader().load('https://aerotwist.com/static/tutorials/creating-particles-with-three-js/images/particle.png')
	var material = new THREE.PointsMaterial( { size:10.0, color: 0xFFFFFF, sizeAttenuation: false, map:texture, transparent:true, blending: THREE.AdditiveBlending} );
	points = new THREE.Points( geometry, material );
	//scene.add( points );


	// TODOcreate planets
	// TODO create moons
	var gui = new dat.GUI();

	for(let x = 0; x < planets.length; x++) {
		//console.log('adding ' + planets[x].name + ' to (' + planets[x].x + ',' + planets[x].y + ',' + planets[x].z +')' + ' traits ' + planets[x].traits)
		let planet = new THREE.SphereGeometry(planets[x].radius, 32, 32);
		let planetMaterial = new THREE.MeshBasicMaterial({map: new THREE.TextureLoader().load(planets[x].texture)});
		let mesh = (new THREE.Mesh(planet, planetMaterial));
		mesh.planetName = planets[x].name;
		mesh.position.x = planets[x].x;
		mesh.position.y = planets[x].y;
		mesh.position.z = planets[x].z;
		mesh.orbital_period = planets[x].traits['rotation_speed']
		console.log(planets[x]);
		if (planets[x].traits['tilt'] != undefined)
			mesh.rotateX(planets[x].traits['tilt']);
		if (planets[x].traits['orbital_data'] != undefined)
			createOrbit(planets[x].traits['orbital_data'])
		mesh.setCamera = ()=>{
			controls.target.set(mesh.position.x, mesh.position.y, mesh.position.z)
		}
		gui.add(mesh, 'setCamera').name(planets[x].name);
		meshes.push(mesh);
		scene.add(mesh);
	}


	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );

	container.appendChild( renderer.domElement );

	window.addEventListener( 'resize', onWindowResize, false );
	animate();

}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

function createOrbit( orbit_data ){
	var radius = orbit_data['circumference'] / (2 * 3.14);
	var material = new THREE.LineBasicMaterial({
		color: 0xFFFFFF, transparent:true, opacity:0.45
	});

	var geometry = new THREE.Geometry();
	for (let i = 0; i <= 360; i++){
		let y = Math.sin(i * Math.PI / 180) * radius;
		let x = Math.cos(i * Math.PI / 180) * radius;
		geometry.vertices.push(
			new THREE.Vector3( x, 0, y )
		);
	}
	var line = new THREE.Line( geometry, material );
	scene.add( line );
}

function animate() {
	requestAnimationFrame( animate );
	controls.update();
	for (let x = 0; x < meshes.length; x++)
		meshes[x].rotateY(0.0174533 / (meshes[x].orbital_period * 5));
	render();

}

function render() {
	//var magnitude = Math.sqrt(points.position.x*points.position.x + points.position.y*points.position.y + points.position.z*points.position.z)
	for (let x = 0; x < lods.length; x++)
		lods[x].update(camera);
	renderer.render( scene, camera );

}