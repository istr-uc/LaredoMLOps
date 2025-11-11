import React, { useState } from 'react'
import CustomButton from '@components/CustomButton'
import CustomModal from '@components/CustomModal'
import preprocessingMethods from '@assets/data/preprocessingMethods.json'
import helpIcon from '@assets/images/helpIcon.svg'
import deleteIcon from '@assets/images/deleteIcon.svg'
import { validateAndParseParam } from '@utils/paramsUtils'
import DropColumnsSelection from '@pages/ModelCreation/DatasetPreprocessing/DropColumnsSelection'

function DatasetPreprocessing({columns, dropColumns, setDropColumns, selectedMethods, setSelectedMethods, 
    columnsDropSelected, setColumnsDropSelected, onNextStep}) {

    const [showModal, setShowModal] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState('')
    const [selectedMethod, setSelectedMethod] = useState('')
    const [selectedParams, setSelectedParams] = useState({})
    const [errors, setErrors] = useState({})

    const openModal = () => {
        setShowModal(true)
    }

    const closeModal = () => {
        setErrors({})
        setShowModal(false)
    }

    const handleOnCancel = () => {
        setSelectedMethods({})
        setColumnsDropSelected(false)
    }

    const onDelete = (method) => {
        setSelectedMethods(prev => {
            const updated = { ...prev };
            delete updated[method];
            return updated;
        });
    }

    const handleCellClick = (category, method, params) => {
        if (params != null && Object.keys(params).length > 0) {
            openModal()
            setSelectedCategory(category)
            setSelectedMethod(method)
            setSelectedParams(params)
        } else {
            const methodCategory = preprocessingMethods[category].methods[method].strategy
            if (preprocessingMethods[category].multiple_selection == false) {
                const prevMethod = Object.keys(selectedMethods).find(method => preprocessingMethods[category].methods[method])
                const newSelectedMethods = { ...selectedMethods }
                delete newSelectedMethods[prevMethod]
                setSelectedMethods({ ...newSelectedMethods, [method]: { strategy: methodCategory } })
            } else {
                setSelectedMethods({ ...selectedMethods, [method]: { strategy: methodCategory } })
            }
        }
    }

    const applyParams = () => {
        const validatedParams = {}
        let hasError = false
        const methodParams = preprocessingMethods[selectedCategory].methods[selectedMethod].params
        const methodCategory = preprocessingMethods[selectedCategory].methods[selectedMethod].strategy

        Object.entries(selectedParams).forEach(([paramName, value]) => {
            const param = methodParams[paramName]
            const { isValidParameter, parsedValue } = validateAndParseParam(paramName, value, param.type, param.enum)
            if (!isValidParameter) {
                setErrors(prevErrors => ({
                    ...prevErrors,
                    [paramName]: 'Invalid value'
                }))
                hasError = true
            } else {
                validatedParams[paramName] = parsedValue
            }
        })

        if (!hasError) {
            if (!preprocessingMethods[selectedCategory].multiple_selection) {
                const prevMethod = Object.keys(selectedMethods).find(method => preprocessingMethods[selectedCategory].methods[method])
                const newSelectedMethods = { ...selectedMethods }
                delete newSelectedMethods[prevMethod]
                setSelectedMethods({ ...newSelectedMethods, [selectedMethod]: {strategy: methodCategory, params : validatedParams} })
            } else {
                setSelectedMethods({ ...selectedMethods, [selectedMethod]: {strategy: methodCategory, params : validatedParams} })
            }
            closeModal()
        }
    }

    const handleChange = (paramName, value) => {
        setSelectedParams({ ...selectedParams, [paramName]: value })
        setErrors(prevErrors => ({
            ...prevErrors,
            [paramName]: ''
        }))
    }

    return(
        <>
            { columnsDropSelected ? (
                <div className='flex flex-col items-center justify-center'>
                    <h1 className='text-6xl font-bold mt-8'>Customize preprocessing pipeline</h1>
                    <strong className='mt-5'>Click on the techniques you want to use and specify the parameters to construct your pipeline.</strong>
                    <div className='grid grid-cols-2 w-3/4'>
                        <table className='border border-white mt-5 w-fit mx-auto'>
                        {Object.entries(preprocessingMethods).map(([category]) => (
                            <React.Fragment key={category}>
                                <tbody>
                                    <tr>
                                        <td className='bg-gray-800 text-white font-bold px-5 py-1' colSpan='2'>{category.replace(/_/g, ' ')}</td>
                                    </tr>
                                    {Object.entries(preprocessingMethods[category].methods).map(([method, methodData]) => (
                                        <tr key={method} className='bg-gray-800 hover:bg-transparent cursor-pointer'>
                                            <td className='pl-3'>
                                                <a href={methodData.url} target='_blank' rel='noopener noreferrer'>
                                                    <img src={helpIcon} alt="help icon" className='inline-block' />
                                                </a>
                                            </td>
                                            <td
                                                className='p-1'
                                                onClick={() => handleCellClick(category, method, methodData.params)}
                                            >
                                                <span>{method}</span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </React.Fragment>
                        ))}
                        </table>
                        <div className='flex flex-col items-center'>
                            <table className='bg-gray-800 border border-white mt-5 w-96'>
                                <thead>
                                    <tr>
                                        <td className='text-white text-lg font-bold px-5 py-1'>Pipeline</td>
                                    </tr>
                                </thead>
                                <tbody>
                                {Object.keys(selectedMethods).map((method, index) => {
                                    const paramsWithoutStrategy = { ...selectedMethods[method] }
                                    delete paramsWithoutStrategy.strategy
                                    return (
                                        <tr key={index}>
                                            <td className='flex px-5 py-1'>
                                                {method} {JSON.stringify(paramsWithoutStrategy)}
                                                <img className='ml-auto cursor-pointer' src={deleteIcon} onClick={() => onDelete(method)} alt='Delete' />
                                            </td>
                                        </tr>
                                    )
                                })}
                                </tbody>
                            </table>
                            <div className='flex flex-row mt-5 mb-5'>
                                <CustomButton className='mr-3' onClick={onNextStep}>Choose your algorithm</CustomButton>
                                <CustomButton onClick={handleOnCancel}>Cancel</CustomButton>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <DropColumnsSelection 
                    columns={columns} 
                    selectedMethods={selectedMethods}
                    setSelectedMethods={setSelectedMethods}
                    setColumnsDropSelected={setColumnsDropSelected}
                    dropColumns={dropColumns}
                    setDropColumns={setDropColumns}
                />
            )}

            <CustomModal isOpen={showModal} onClose={closeModal}>
                <h2 className='text-5xl text-white font-semibold'>{selectedMethod} Parameters</h2>
                {Object.entries(selectedParams).map(([paramName]) => (
                    <div className='flex flex-col mt-4' key={paramName}>
                        <label htmlFor={paramName} className='text-2xl mb-1'>
                            {paramName}
                        </label>
                        <input
                            type='text'
                            id={paramName}
                            className='text-xl border border-white bg-gray-800 rounded-md p-2'
                            onChange={(e) => handleChange(paramName, e.target.value)}
                        />
                        <strong className='text-red-500'>{errors[paramName]}</strong>
                    </div>
                ))}
                <CustomButton className='mt-6' onClick={applyParams}>Apply</CustomButton>
            </CustomModal>
        </>
    )
}

export default DatasetPreprocessing