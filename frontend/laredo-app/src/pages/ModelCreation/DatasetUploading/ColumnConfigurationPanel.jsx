import { useEffect, useState } from 'react'
import axios from 'axios'
import CustomButton from '@components/CustomButton'

function ColumnConfigurationPanel({preview, columns, columnsDataType, setColumnsDataType, target, setTarget, onNextStep, onReject}) {

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        try {
            const datasetJSON = preview
            // const apiIp = import.meta.env.VITE_API_IP
            // const apiPort = import.meta.env.VITE_API_PORT
            // const apiUrl = `http://${apiIp}:${apiPort}/column-types`
            const apiUrl = `/api/column-types`
            const response = await axios.post(apiUrl, {
                datasetJSON
            })
            setColumnsDataType(response.data)
        } catch (error) {
            console.error('Error fetching data:', error)
        }
    }
    const [errors, setErrors] = useState({})
    const [targetError, setTargetError] = useState(null)

    const handleDataTypeChange = (column, event) => {
        setColumnsDataType(prevState => ({
            ...prevState,
            [column]: event.target.value
        }))

        setErrors(errors => ({
            ...errors,
            [column]: ''
        }))
    }

    const handleTargetChange = (column) => {
        setTarget(column)
        setTargetError(null)
    }

    const handleOnNextStep = () => {
        const newErrors = {}
      
        for (const column in columnsDataType) {
            if (columnsDataType[column] === '') {
                newErrors[column] = 'Please select a data type.'
            }
        }
      
        setErrors(newErrors)
      
        if (!target) {
            setTargetError('Please choose a target column')
        }
      
        if (Object.keys(newErrors).length === 0 && target) {
            onNextStep()
        }
      }
      


    return(
        <>
            <div className='grid grid-cols-2 h-[70vh] w-full mt-12'>
                <div className='w-1/2 mx-auto flex justify-center'>
                    <table className='w-fit text-center'>
                        <thead>
                            <tr>
                                <th className='text-white px-14 py-5'>Column name</th>
                                <th className='text-white px-9 py-5'>Data type</th>
                                <th className='text-white px-9 py-5'>
                                    {targetError && (<p className='text-red-500'>{targetError}</p>)}
                                    Target
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {columns.map((column, index) => (
                                <tr className='justify-center border-b border-gray-800' key={index}>
                                    <td>
                                        <label htmlFor={column}>{column}</label>
                                    </td>
                                    <td>
                                        <select className='text-white rounded-sm border border-white bg-gray-800 my-2 py-1 w-fit'
                                                value={columnsDataType[column]}
                                                onChange={(event) => handleDataTypeChange(column, event)}
                                        >
                                        <option value=''>Select a data type...</option>
                                        <option value='int64'>Integer</option>
                                        <option value='float64'>Float</option>
                                        <option value='object'>String</option>
                                        <option value='datetime64[ns]'>DateTime (ns)</option>
                                        <option value='datetime64[s]'>DateTime (s)</option>
                                        </select>
                                        {errors[column] && (
                                            <p className='text-red-500'>{errors[column]}</p>
                                        )}
                                    </td>
                                    <td>
                                        <input
                                            className='ml-4'
                                            type='radio'
                                            id={column}
                                            value={column}
                                            name={'target'}
                                            checked={target === column}
                                            onChange={() => handleTargetChange(column)}
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className='flex flex-col justify-start text-right mx-auto mt-52'>
                    <div className='sticky top-1/4 items-end text-right'>
                        <h1 className='text-5xl font-bold'>
                            Set column data type <br/> 
                            and column target
                        </h1>
                        <strong className='mt-3 block'>
                                Select the data type for each column of your dataset, <br/>
                                and identify the target column from the available options.</strong>
                        <div className='flex justify-end mt-5'>
                            <CustomButton className='mr-6' onClick={handleOnNextStep}>Preprocess</CustomButton>
                            <CustomButton onClick={onReject}>Cancel</CustomButton>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default ColumnConfigurationPanel