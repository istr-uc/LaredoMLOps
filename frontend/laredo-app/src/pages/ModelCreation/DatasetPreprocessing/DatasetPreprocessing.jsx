import React, { useState } from 'react'
import CustomButton from '@components/CustomButton'
import CustomModal from '@components/CustomModal'
import preprocessingMethods from '@assets/data/preprocessingMethods.json'
import helpIcon from '@assets/images/helpIcon.svg'
import deleteIcon from '@assets/images/deleteIcon.svg'
import { validateAndParseParam } from '@utils/paramsUtils'
import DropColumnsSelection from '@pages/ModelCreation/DatasetPreprocessing/DropColumnsSelection'

function DatasetPreprocessing({columns, dropColumns, setDropColumns, selectedMethods, setSelectedMethods, 
    columnsDropSelected, setColumnsDropSelected, target, usableColumns, setUsableColumns, onNextStep}) {
    
    const [showModal, setShowModal] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState('')
    const [selectedMethod, setSelectedMethod] = useState('')
    const [selectedParams, setSelectedParams] = useState({})
    const [errors, setErrors] = useState({})
    
    

    const openModal = () => {
        // if usable columns are empty or have changed, update them
        
        if (usableColumns.length === 0) {
            setUsableColumns(columns.filter(col => !(dropColumns.includes(col) || col === target)))
        } else if (usableColumns.length !== columns.filter(col => !(dropColumns.includes(col) || col === target)).length) {
            setUsableColumns(columns.filter(col => !(dropColumns.includes(col) || col === target)))
        }
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

    const getOrderWarning = (selectedCategory) => {
        const currentOrder = preprocessingMethods[selectedCategory].order
        
        // Obtener el orden máximo de los métodos ya seleccionados
        let maxSelectedOrder = 0
        Object.entries(selectedMethods).forEach(([methodName]) => {
            // Encontrar a qué categoría pertenece este método
            for (const [categoryName, categoryData] of Object.entries(preprocessingMethods)) {
                if (categoryData.methods[methodName]) {
                    maxSelectedOrder = Math.max(maxSelectedOrder, categoryData.order)
                    break
                }
            }
        })
        
        // Si el orden actual es menor que el máximo seleccionado, es una violación
        if (currentOrder < maxSelectedOrder) {
            const violatedCategory = Object.entries(preprocessingMethods).find(([_, data]) => data.order === maxSelectedOrder)
            return { categoryName: violatedCategory[0], order: maxSelectedOrder }
        }
        return null
    }

    const handleCellClick = (category, method, params) => {
        const warning = getOrderWarning(category)
        if (warning) {
            alert(`⚠️ Warning: Adding "${category.replace(/_/g, ' ')}" (Step ${preprocessingMethods[category].order}) after "${warning.categoryName.replace(/_/g, ' ')}" (Step ${warning.order}) violates the recommended order.`)
        }
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
            // If the parameter type is 'column' or 'column-list', set its enum to the list of columns
            if (param.type === 'column' || param.type === 'column-list') {
                param.enum = usableColumns
            }
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
                        {Object.entries(preprocessingMethods)
                            .sort(([,a], [,b]) => a.order - b.order)
                            .map(([category]) => (
                            <React.Fragment key={category}>
                                <tbody>
                                    <tr>
                                        <td className='bg-gray-800 text-white font-bold pl-3'>
                                            <span className='inline-flex items-center justify-center text-white rounded-full font-bold'>{preprocessingMethods[category].order}</span>
                                        </td>
                                        <td className='bg-gray-800 text-white font-bold p-1'>
                                            {category.replace(/_/g, ' ')}
                                        </td>
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
                                <CustomButton onClick={handleOnCancel}>Back</CustomButton>
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
                <p className='text-sm text-gray-400 mt-2'>Step {selectedCategory && preprocessingMethods[selectedCategory].order} - {selectedCategory && selectedCategory.replace(/_/g, ' ')}</p>
                {Object.entries(selectedParams).map(([paramName]) => (
                    <div className='flex flex-col mt-4' key={paramName}>
                        <label htmlFor={paramName} className='text-2xl mb-1'>
                            {paramName}
                        </label>
                        
                        { // If the parameter type is 'column', render a dropdown with the column names 
                        preprocessingMethods[selectedCategory].methods[selectedMethod].params[paramName].type === 'column' ?
                        <select
                            id={paramName}
                            className='text-xl border border-white bg-gray-800 rounded-md p-2'
                            onChange={(e) => handleChange(paramName, e.target.value)}
                        >
                            <option value=''>Select an option</option>
                            {usableColumns.map((option) => (
                                <option key={option} value={option}>{option}</option>
                            ))}
                        </select>
                        : // If the parameter type is 'column-list', render a list of checkboxes
                        preprocessingMethods[selectedCategory].methods[selectedMethod].params[paramName].type === 'column-list' ?
                        <div className='max-h-40 overflow-y-auto border border-white rounded-md p-2'>
                            {usableColumns.map((option) => (
                                <div key={option} className='flex items-center mb-2'>
                                    <input
                                        type='checkbox'
                                        id={`${paramName}-${option}`}
                                        className='mr-2'
                                        checked={Array.isArray(selectedParams[paramName]) && selectedParams[paramName].includes(option)}
                                        onChange={(e) => {
                                            const currentValues = Array.isArray(selectedParams[paramName]) ? selectedParams[paramName] : [];
                                            const newValue = e.target.checked
                                                ? [...currentValues, option]
                                                : currentValues.filter(v => v !== option);
                                            handleChange(paramName, newValue);
                                        }}
                                    />
                                    <label htmlFor={`${paramName}-${option}`} className='text-xl'>
                                        {option}
                                    </label>
                                </div>
                            ))}
                        </div>
                        : // Otherwise, render a text input
                        <input
                            type='text'
                            id={paramName}
                            className='text-xl border border-white bg-gray-800 rounded-md p-2'
                            onChange={(e) => handleChange(paramName, e.target.value)}
                        />
                        }
                        <strong className='text-red-500'>{errors[paramName]}</strong>
                    </div>
                ))}
                <CustomButton className='mt-6' onClick={applyParams}>Apply</CustomButton>
            </CustomModal>
        </>
    )
}

export default DatasetPreprocessing