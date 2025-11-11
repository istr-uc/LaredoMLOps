import { FileUploader } from 'react-drag-drop-files'
import Papa from 'papaparse'
import DatasetChecking from '@pages/ModelCreation/DatasetUploading/DatasetChecking'
import ColumnConfigurationPanel from '@pages/ModelCreation/DatasetUploading/ColumnConfigurationPanel'
import uploadIcon from '@assets/images/uploadIcon.svg' 

function DatasetUploading({datasetFile, setDatasetFile, columnsDataType, setColumnsDataType, preview, setPreview,
    datasetUploaded, setDatasetUploaded, columns, setColumns, hasHeader, setHasHeader, columnsTypeIndicated,
    setColumnsTypeIndicated, target, setTarget, onNextStep}) {    

    const handleChange = (file) => {
        setDatasetFile(file)
        Papa.parse(file, {
            header: hasHeader,
            dynamicTyping: true,
            skipEmptyLines: true,
            preview: 6,
            complete: function (results) {
                setPreview(results.data)
                let columns_aux;
                if (hasHeader) {
                    columns_aux = results.meta.fields
                    setColumns(columns_aux);
                    const initialColumnsDataType = {};
                    columns_aux.forEach(column => {
                        initialColumnsDataType[column] = ''
                    })
                    setColumnsDataType(initialColumnsDataType)
                } else {
                    columns_aux = []
                    for (let i = 0; i < results.data[0].length; i++) {
                        columns_aux.push(`${i}`)
                    }
                    setColumns(columns_aux)
                    const initialColumnsDataType = {}
                    columns_aux.forEach(column => {
                        initialColumnsDataType[column] = ''
                    })
                    setColumnsDataType(initialColumnsDataType)
                }
                setTarget(columns_aux[columns_aux.length - 1])
            },
        })
    }

    const onConfirm = () => {
        setDatasetUploaded(true)
        if (datasetUploaded) {
            setColumnsTypeIndicated(true)
        }
    }

    const onReject = () => {
        setColumnsTypeIndicated(false)
        setDatasetUploaded(false)
        setDatasetFile(null)
        setColumnsDataType({})
    }

    return(
        <>
            {datasetUploaded ? (
                <ColumnConfigurationPanel 
                    preview={preview} 
                    columns={columns} 
                    columnsDataType={columnsDataType} 
                    setColumnsDataType={setColumnsDataType} 
                    target={target} 
                    setTarget={setTarget} 
                    onNextStep={onNextStep} 
                    onReject={onReject}
                />
            ) : (
                datasetFile ? (
                    <DatasetChecking preview={preview} columns={columns} onConfirm={onConfirm} onReject={onReject}/>
                ) : (
                    <>
                        <div className='grid grid-cols-2 h-[70vh] w-full mt-12'>

                            <div className='flex flex-col'>
                                <div className='flex justify-center'>
                                    <input 
                                        className='h-6 w-6 mr-2'
                                        type='checkbox' 
                                        id='checkbox' 
                                        checked={hasHeader} 
                                        onChange={() => setHasHeader(!hasHeader)}
                                    />
                                    <label htmlFor='checkbox' className='text-white text-lg'>Header included</label>
                                </div>

                                <div className='grow mt-6'>
                                    <FileUploader handleChange={handleChange} name="file" types={['csv']} dropMessageStyle={{ marginRight: 'auto', marginLeft: 'auto', width: '91.666667%' }} hoverTitle={" "}>
                                        <div className='flex flex-col justify-center items-center border-2 border-dashed rounded-md border-cyan-400 cursor-pointer h-full w-11/12 mx-auto bg-gray-800'>
                                            <img src={uploadIcon} alt='Upload file icon' className='w-20 h-20'/>
                                            <strong className='text-white mx-auto text-center text-4xl mt-12'>Drop your dataset here <br/>or click to upload</strong>  
                                            <p className='mt-3'>Support: *.csv</p>  
                                        </div>
                                    </FileUploader>
                                </div>
                            </div>


                            <div className='flex flex-col justify-center mx-auto text-right'>
                                <h1 className='text-5xl font-bold'>Choose your dataset</h1>
                                <strong className='mt-5'>Upload your dataset to start building your model.</strong>
                            </div>
                        </div>
                    </>
                )
            )}
        </>
    )
}

export default DatasetUploading