import { Canvas } from '@react-three/fiber';
import { Line, OrbitControls, Plane, Sphere } from '@react-three/drei';

const Trajectory3D = ({ points, targetPosition, initialPosition, animationState }) => {
    return (
        <Canvas camera={{ position: [0, 5, 20], fov: 75 }}>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            {points.length > 0 && (
                <Line 
                    points={points} 
                    color={animationState?.lineColor || "red"} 
                    lineWidth={animationState?.lineWidth || 5} 
                />
            )}
            <Plane args={[100, 100]} position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                <meshStandardMaterial attach="material" color="green" />
            </Plane>
            <mesh position={targetPosition}>
                <Sphere args={[0.5, 32, 32]} />
                <meshStandardMaterial color={animationState?.targetColor || "blue"} />
            </mesh>
            <mesh position={initialPosition}>
                <Sphere args={[0.5, 32, 32]} />
                <meshStandardMaterial color={animationState?.initialColor || "yellow"} />
            </mesh>
            <axesHelper args={[10]} />
            <OrbitControls maxPolarAngle={Math.PI / 2} minPolarAngle={0} />
        </Canvas>
    );
};

export default Trajectory3D;
