import React from 'react'
import CustomButton from '@components/CustomButton'


function DatasetChecking({preview, columns, onConfirm, onReject}) {

    return(
        <>
            <div className='grid grid-cols-2 h-[70vh] w-full mt-12'>
                <div className='max-w-full overflow-x-auto mx-auto my-auto w-11/12'>
                    <table className='w-full text-center bg-gray-800'>
                        <thead className='text-white font-bold border-t border-white'>
                            <tr>
                                {columns.map((column, index) => (
                                    <th key={index} className='border-l border-r border-white px-4 py-2'>{column}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {preview.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                    {Object.values(row).map((value, columnIndex) => (
                                        <td key={columnIndex} className='border-l border-r border-white px-4 py-2'>{value}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className='flex flex-col justify-center mx-auto text-right'>
                    <h1 className='text-5xl font-bold'>Check uploaded dataset</h1>
                    <strong className='mt-5'>
                        Check that this is the dataset you want to use.<br/>
                        Is this the right one?
                    </strong>
                    <div className='flex justify-end mt-5'>
                        <CustomButton className='text-xl w-36 mr-6' onClick={onConfirm}>Yes</CustomButton>
                        <CustomButton className='text-xl w-36' onClick={onReject}>No</CustomButton>
                    </div>
                </div>
            </div>
        </>
    )
}

export default DatasetChecking