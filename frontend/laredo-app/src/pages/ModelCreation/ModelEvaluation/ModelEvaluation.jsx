import React from "react"
import { useNavigate } from 'react-router-dom'
import CustomButton from '@components/CustomButton'

function ModelEvaluation({metrics, modelName}) {

    
    const navigate = useNavigate()
    const goHome = () => {
        navigate('/')
    }
    const goModelDetails = () => {
        navigate(`/models/${modelName}`)
    }

    return(
        <>
            <div className='grid grid-cols-2 h-[70vh] w-full'>
                <div className='flex flex-col justify-center items-center'>
                    <table className='bg-gray-800 border-white rounded-xl'>
                        <thead className='text-white'>
                            <tr className='border-b '>
                                <th className='w-48 p-3 text-2xl border-r'>Metric</th>
                                <th className='w-48 p-3 text-2xl'>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                        {Object.entries(metrics).map(([metricName, metricValue]) => (
                            <tr key={metricName} className='border-t'>
                                <td className='w-48 p-3 text-xl border-r'>{metricName}</td>
                                <td className='w-48 p-3 text-xl'>{metricValue}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
                <div className='flex flex-col justify-center items-end text-right mx-auto'>
                    <h1 className='text-6xl font-bold'>Evaluate your model</h1>
                    <strong className='mt-5'>Explore metrics of the generated model for informed analysis.</strong>
                    <div className='flex flex-row mt-5 mb-5'>
                        <CustomButton className='mx-2 text-lg mt-5 w-fit' onClick={goHome}>Finish</CustomButton>
                        <CustomButton className='mx-2 text-lg mt-5 w-fit' onClick={goModelDetails}>More Details</CustomButton>
                    </div>
                    
                </div>
            </div>
        </>
    )
}

export default ModelEvaluation