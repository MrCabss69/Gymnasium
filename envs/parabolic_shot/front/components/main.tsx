"use client";
import React, { useState, useCallback } from 'react';
import Trajectory3D from '@/components/trajectory';
import InputForm from '@/components/ui/input_form';
import axios from 'axios';

function ControlButtons({ handleEnvironment, fire, loading, inputs }) {
    return (
        <div className="space-x-4">
            <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded shadow-lg transition duration-300 ease-in-out disabled:opacity-50" onClick={() => handleEnvironment('reset')} disabled={loading}>
                Reset
            </button>
            
            <button className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded shadow-lg transition duration-300 ease-in-out disabled:opacity-50" onClick={fire} disabled={loading || !inputs.v0 || inputs.angulo_x <= 0 || inputs.angulo_y <= 0}>
                Fire
            </button>

            <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded shadow-lg transition duration-300 ease-in-out disabled:opacity-50" onClick={() => handleEnvironment('close')} disabled={loading}>
                Close
            </button>
        </div>
    );
}

function MainView() {
    const [inputs, setInputs] = useState({
        v0: 30, angulo_x: 45, angulo_y: 45, x0: 0, y0: 0, z0: 0, resistencia_viento: 0
    });
    const [trajectory, setTrajectory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [lastSimulation, setLastSimulation] = useState([]);
    const [animationState, setAnimationState] = useState({});

    const handleChange = useCallback((e) => {
        const { name, value } = e.target;
        const numValue = parseFloat(value);
        setInputs(prevInputs => ({ ...prevInputs, [name]: isNaN(numValue) ? 0 : numValue }));
    }, []);

    const handleEnvironment = async (command) => {
        setLoading(true);
        try {
            await axios.get(`http://localhost:5000/${command}`);
            if (command === 'reset' || command === 'close') {
                setTrajectory([]);
            }
            setLoading(false);
        } catch (error) {
            console.error(`Error in ${command}:`, error);
            setLoading(false);
        }
    };

    const fire = async () => {
        if (loading || !inputs.v0 || inputs.angulo_x <= 0 || inputs.angulo_y <= 0) {
            alert("Please enter valid values for v0, angulo_x, and angulo_y.");
            return;
        }
        setLoading(true);
        try {
            const action = { angle_x: inputs.angulo_x, angle_y: inputs.angulo_y, v0: inputs.v0 };
            console.log(action);
            const { data } = await axios.post('http://localhost:5000/step', action);
            console.log(data);
            setTrajectory(data.trajectory);
        } catch (error) {
            console.error("Error firing:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="main-view mx-auto px-4 py-8 md:px-8 lg:px-16">
            <div className="flex flex-col space-y-6 items-center justify-center">
                <h1>Projectile Trajectory Simulator</h1>
                <InputForm inputs={inputs} handleChange={handleChange} />
                <ControlButtons handleEnvironment={handleEnvironment} fire={fire} loading={loading} inputs={inputs} />
                <Trajectory3D points={trajectory} targetPosition={[inputs.x0, 0, inputs.z0]} initialPosition={[inputs.x0, 0, inputs.z0]} animationState={animationState} />
            </div>
        </div>
    );
}

export default MainView;
