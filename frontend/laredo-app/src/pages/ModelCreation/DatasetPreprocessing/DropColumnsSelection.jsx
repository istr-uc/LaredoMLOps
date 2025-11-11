import React from "react"
import CustomButton from "@components/CustomButton"

function DropColumnsSelection({columns, selectedMethods, setSelectedMethods, dropColumns, setDropColumns, setColumnsDropSelected}) {

    const handleCheckboxClick = (column) => {
        if (dropColumns.includes(column)) {
            setDropColumns(dropColumns.filter((col) => col !== column))
        } else {
            setDropColumns([...dropColumns, column])
        }
    }

    const handleOnContinue = () => {
        if (dropColumns.length != 0) {
            const newSelectedMethods = { ...selectedMethods }
            newSelectedMethods[`drop`] = { strategy: 'DropStrategy', params: { dropColumns } }
            setSelectedMethods(newSelectedMethods)
        }


        setColumnsDropSelected(true)
    }

    return(
        <>
            <div className='grid grid-cols-2 h-[70vh] w-full mt-12'>
                <div className='w-1/2 mx-auto flex justify-center'>
                    <table className='w-fit text-center'>
                        <tbody>
                            {columns.map((column, index) => (
                                <tr key={index}>
                                    <td className='border-b border-gray-800 py-2 px-14'>
                                        <label htmlFor={column} className='text-cyan-400'>{column}</label>
                                    </td>
                                    <td className='border-b border-gray-800 py-2 pr-14'>
                                        <input
                                            className='ml-3 h-4 w-4 '
                                            type='checkbox'
                                            id={column}
                                            checked={dropColumns.includes(column)}
                                            onChange={() => handleCheckboxClick(column)}
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className='flex flex-col justify-start text-right mx-auto mt-52'>
                    <div className='sticky top-1/4 items-end text-right'>
                        <h1 className='text-5xl font-bold'>Select columns to drop</h1>
                        <strong className='mt-3 block'>Choose the columns you want to remove from your dataset.</strong>
                        <CustomButton className='mt-3 text-xl w-36' onClick={handleOnContinue}>
                            Continue
                        </CustomButton>
                    </div>
                </div>
            </div>
        </>
    )
}

 export default DropColumnsSelection