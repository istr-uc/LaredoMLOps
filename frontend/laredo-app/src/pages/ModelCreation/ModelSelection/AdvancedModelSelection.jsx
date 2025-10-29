import React, { useState , useEffect } from 'react'
import algorithmData from '@assets/data/algorithmParameters.json'
import CustomButton from '@components/CustomButton'
import infoIcon from '@assets/images/infoIcon.svg'
import { validateAndParseParam } from '@utils/paramsUtils'

function AdvancedModelSelection({algorithm, setAlgorithm, parametersValue, setParametersValue, problemType, onNextStep}) {

    const [errors, setErrors] = useState({})

    useEffect(() => {
        if (algorithm) {
            const defaultValues = {}
            const parameters = algorithmData[problemType][algorithm].parameters
            Object.keys(parameters).forEach(parameterName => {
                defaultValues[parameterName] = parameters[parameterName].default
            });
            setParametersValue(defaultValues)
        }
    }, [algorithm])

    const handleSelectAlgorithm = (event) => {
        setAlgorithm(event.target.value)
        setErrors({})
    }

    const handleParameterChange = (parameterName, event) => {
        const value = event.target.value;
        setParametersValue(prevState => ({
            ...prevState,
            [parameterName]: value
        }))

        setErrors(prevErrors => ({
            ...prevErrors,
            [parameterName]: ''
        }))
    }

    function getTypeLabel(type, enumValues) {
        if (Array.isArray(type)) {
            let typeLabel = type.map(type => {
                if (type === 'string' && enumValues && enumValues.length > 0) {
                    return `${type} [${enumValues.map(value => `'${value}'`).join(', ')}]`
                } else {
                    return type
                }
            })
            return typeLabel.join(', ')
        } else {
            if (type === 'string' && enumValues && enumValues.length > 0) {
                return `${type} [${enumValues.map(value => `'${value}'`).join(', ')}]`
            } else {
                return type
            }
        }
    }

    const validateParameters = () => {
        const parameters = algorithmData[problemType][algorithm].parameters
        let isValid = true
        const parsedParametersValue = {}

        Object.keys(parameters).forEach(parameterName => {
            const value = parametersValue[parameterName]
            const parameter = parameters[parameterName]
            const {isValidParameter, parsedValue} = validateAndParseParam(parameterName, value, parameter.type, parameter.enum)
            if (!isValidParameter) {
                isValid = false
                setErrors(prevErrors => ({
                    ...prevErrors,
                    [parameterName]: 'Invalid value'
                }))
            } else {
                parsedParametersValue[parameterName] = parsedValue
            }
        })

        return {isValid, parsedParametersValue}
    }

    const handleNextStep = () => {
        const {isValid, parsedParametersValue} = validateParameters()

        if (isValid) {
            setParametersValue(parsedParametersValue)
            onNextStep()
        }
    }

    return(
        <>
            <div className='grid grid-cols-2'>
                <div>
                    <div className='flex justify-center items-center mt-12'>

                        <strong className='mr-4 text-2xl'>Algorithm:</strong>
                        <select className='cursor-pointer text-white rounded-sm border border-white bg-gray-800 py-1 text-xl w-fit' 
                            value={algorithm} onChange={handleSelectAlgorithm}>

                            <option value="" className='cursor-pointer' disabled>Select an algorithm...</option>
                                
                            {Object.keys(algorithmData[problemType]).map((algorithmName) => (
                                <option className='cursor-pointer' key={algorithmName} value={algorithmName}>
                                    {algorithmName}
                                </option>
                            ))}
                            
                        </select>
                            
                    </div>
                    <div className="flex justify-center items-center mt-6">
                        {algorithm && (
                            <div>
                                <h2 className='mt-5 text-xl'>Parameters:</h2>
                                <table className='my-5 bg-transparent border-white w-full'>
                                    <tbody>
                                        {Object.keys(algorithmData[problemType][algorithm].parameters).map((parameterName) => {
                                            const parameterData = algorithmData[problemType][algorithm].parameters[parameterName]
                                            const defaultValue = parameterData.default
                                            const description = parameterData.description
                                            const type = parameterData.type
                                            const enumValues = parameterData.enum
                                            return (
                                                <tr key={parameterName}>
                                                    <td  className='text-left border-0 border-b-2 border-gray-800 px-2 py-2'>{parameterName}</td>
                                                    <td className='flex border-0 border-b-2 border-gray-800 py-2'>
                                                        <input 
                                                            className='border border-white rounded-sm bg-transparent text-white px-1'
                                                            type="text" 
                                                            value={parametersValue[parameterName] ?? defaultValue ?? ''}
                                                            onChange={(event) => handleParameterChange(parameterName, event)}
                                                        />
                                                        <div className='flex flex-col items-center group relative'>
                                                            <p className='hidden absolute text-white text-xs whitespace-nowrap -top-8 group-hover:block
                                                                            bg-gray-800 p-1 rounded border border-white text-center'>
                                                                {description}<br/>
                                                                Data type: {getTypeLabel(type, enumValues)}
                                                            </p>
                                                            <img src={infoIcon} className='ml-1 cursor-pointer' alt='Information icon' />
                                                        </div>
                                                    </td>
                                                    <td className='text-red-500'>{errors[parameterName]}</td>
                                                </tr>
                                            )
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>

                <div className='flex flex-col justify-start text-right mx-auto mt-40'>
                    <div className='sticky top-1/4 items-end text-right'>                    
                        <h2 className='text-5xl font-bold'>Model creation</h2>
                        <h1 className='text-6xl font-bold'>Advanced</h1>
                        <strong className='mt-5'>Set the model parameters once the algorithm is chosen.</strong>
                        <div className="ml-auto mt-6">
                            <CustomButton className='w-fit text-lg' onClick={handleNextStep}>Train your model</CustomButton>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}
export default AdvancedModelSelection
