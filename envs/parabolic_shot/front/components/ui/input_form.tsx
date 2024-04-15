
function InputForm({ inputs, handleChange }) {
    return (
        <div className="grid grid-cols-3 gap-4">
            {Object.keys(inputs).map((inputName) => (
                <input
                    key={inputName}
                    name={inputName}
                    type="number"
                    value={inputs[inputName]}
                    onChange={handleChange}
                    className="border p-2 rounded shadow bg-white text-gray-800"
                    placeholder={`Enter ${inputName.replace('_', ' ')}`}
                />
            ))}
        </div>
    );
};

export default InputForm;