import React, { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import CustomButton from '@components/CustomButton'
import DatasetPreprocessing from '@pages/ModelCreation/DatasetPreprocessing/DatasetPreprocessing'
import DatasetUploading from '@pages/ModelCreation/DatasetUploading/DatasetUploading'
import ModelSelection from '@pages/ModelCreation/ModelSelection/ModelSelection'
import ModelEvaluation from '@pages/ModelCreation/ModelEvaluation/ModelEvaluation'
import algorithmData from '@assets/data/algorithmParameters.json'
import Papa from 'papaparse'
import axios from 'axios'



const Steps = {
    Dataset: 'Dataset',
    Preprocessing: 'Preprocessing',
    Algorithm: 'Algorithm',
    Evaluation: 'Evaluation'
}

const CreationTypes = {
    Basic : 'BASIC',
    Advanced : 'ADVANCED'
}

const BasicProblemTypesEvalMetrics = {
    binary: ['accuracy', 'balanced_accuracy', 'log_loss', 'f1', 'f1_macro', 'f1_micro', 'f1_weighted', 'roc_auc', 'roc_auc_ovo', 'roc_auc_ovo_macro', 'roc_auc_ovo_weighted', 'roc_auc_ovr', 'roc_auc_ovr_macro', 'roc_auc_ovr_micro', 'roc_auc_ovr_weighted', 'average_precision', 'precision', 'precision_macro', 'precision_micro', 'precision_weighted', 'recall', 'recall_macro', 'recall_micro', 'recall_weighted', 'mcc', 'pac_score'],
    multiclass: ['accuracy', 'balanced_accuracy', 'log_loss', 'f1', 'f1_macro', 'f1_micro', 'f1_weighted', 'roc_auc', 'roc_auc_ovo', 'roc_auc_ovo_macro', 'roc_auc_ovo_weighted', 'roc_auc_ovr', 'roc_auc_ovr_macro', 'roc_auc_ovr_micro', 'roc_auc_ovr_weighted', 'average_precision', 'precision', 'precision_macro', 'precision_micro', 'precision_weighted', 'recall', 'recall_macro', 'recall_micro', 'recall_weighted', 'mcc', 'pac_score'],
    regression: ['root_mean_squared_error', 'mean_squared_error', 'mean_absolute_error', 'median_absolute_error', 'mean_absolute_percentage_error', 'r2', 'symmetric_mean_absolute_percentage_error'],
    cluster: []
}


function ModelCreation() {

    const [problemTypes, setProblemTypes] = useState([])
    const [problemType, setProblemType] = useState("")
    const [modelName, setModelName] = useState("")

    const [datasetFile, setDatasetFile] = useState(null)
    const [columnsDataType, setColumnsDataType] = useState({})
    const [preview, setPreview] = useState([])
    const [datasetUploaded, setDatasetUploaded] = useState(false)
    const [columns, setColumns] = useState([])
    const [hasHeader, setHasHeader] = useState(true)
    const [columnsTypeIndicated, setColumnsTypeIndicated] = useState(false)
    const [target, setTarget] = useState("")

    const [columnsDropSelected, setColumnsDropSelected] = useState(false)
    const [dropColumns, setDropColumns] = useState([])
    const [preprocessingMethods, setPreprocessingMethods] = useState({})

    const [creationType, setCreationType] = useState(CreationTypes.Basic)
    const [algorithm, setAlgorithm] = useState("")
    const [parametersValue, setParametersValue] = useState({})
    const [evalMetric, setEvalMetric] = useState('')
    const [preset, setPreset] = useState('')
    const [timeLimit, setTimeLimit] = useState(3600)

    const [metrics, setMetrics] = useState({})

    const [modelNameError, setModelNameError] = useState("")
    const [problemTypeError, setProblemTypeError] = useState("")

    const [activeButton, setActiveButton] = useState('')

    const [hasStarted, setHasStarted] = useState(false)
    const [isTraining, setIsTraining] = useState(false)

    const navigate = useNavigate()

    const activeButtonStyle = 'bg-transparent text-cyan-400 font-bold text-lg py-2 w-40'
    const inactiveButtonStyle = 'bg-gray-900 hover:bg-transparent hover:text-cyan-400 hover:cursor-pointer text-white text-lg py-2 w-40'

    useEffect(() => {
        if (creationType == CreationTypes.Advanced) {
            const uniqueProblemTypes = Array.from(new Set(Object.keys(algorithmData)))
            setProblemTypes(uniqueProblemTypes)
        } else if (creationType == CreationTypes.Basic) {
            const uniqueProblemTypes = Array.from(new Set(Object.keys(BasicProblemTypesEvalMetrics)))
            setProblemTypes(uniqueProblemTypes)
        }
    }, [creationType])

    const goHome = () => {
        navigate('/')
    }

    const goModels = () => {
        navigate('/models')
    }

    const handleHasStarted = () => {
        setModelNameError('')
        setProblemTypeError('')
        if (!modelName) {
            setModelNameError('Please enter a model name')
        }  
        if (!problemType) {
            setProblemTypeError('Please select a problem type')
        }
        if (modelName && problemType) {
            setHasStarted(true)
            setActiveButton(Steps.Dataset)
        }
    }

    const handleActive = (step) => {
        setActiveButton(step)
    }

    const handleNextStep = async () => {
        switch (activeButton) {
            case Steps.Dataset:
                if (creationType == CreationTypes.Advanced) {
                    setActiveButton(Steps.Preprocessing)
                } else if (creationType == CreationTypes.Basic) {
                    setActiveButton(Steps.Algorithm)
                }
                break
            case Steps.Preprocessing:
                setActiveButton(Steps.Algorithm)
                break
            case Steps.Algorithm:
                setIsTraining(true)
                setActiveButton(Steps.Evaluation)
                try {
                    const response = await callAPI()
                    if (response.status == 201) {
                        setMetrics(response.data)
                        setIsTraining(false)
                    } else {
                        setMetrics(null)
                        setIsTraining(false)
                    }
                } catch (error) {
                    console.error('Error calling API:', error)
                    setMetrics(null)
                    setIsTraining(false)
                }
    
                break;
            case Steps.Evaluation:
                break;
            default:
                break;
        }
    }
    
    const callAPI = async() => {
        const datasetJSON = await convertDatasetToJSON(datasetFile)
        
        // const apiIp = import.meta.env.VITE_API_IP
        // const apiPort = import.meta.env.VITE_API_PORT
        // const apiUrl = `http://${apiIp}:${apiPort}/models`
        const apiUrl = `/api/models`
        let params = {
            modelName,
            problemType,
            datasetJSON,
            columnsDataType,
            target,
            preprocessingMethods,
            parametersValue
        }

        if (creationType == CreationTypes.Basic) {
            params = {
                ...params,
                evalMetric,
                preset,
                timeLimit
            }
        } else if (creationType == CreationTypes.Advanced) {
            let strategy = algorithmData[problemType][algorithm].strategy
            params = {
                ...params,
                strategy,
                algorithm
            }
        }
        
        const response = await axios.post(apiUrl, {
            creationType,
            params
        })

        return response
    }
    
    const convertDatasetToJSON = (file) => {
        return new Promise((resolve, reject) => {
            Papa.parse(file, {
                header: hasHeader,
                skipEmptyLines: true,
                dynamicTyping: true,
                complete: (results) => {
                    if (!hasHeader) {
                        const dataWithNumericHeaders = results.data.map((row) => {
                            const newRow = {}
                            row.forEach((value, index) => {
                                newRow[index] = value
                            });
                            return newRow
                        })
                        resolve(dataWithNumericHeaders)
                    } else {
                        resolve(results.data)
                    }
                },
                error: (error) => {
                    reject(error)
                }
            })
        })    
    }

    return(
        <>
            {/* <ChatbotWidget apiUrl="http://localhost:20000" /> */}
            {/* <ChatbotWidget apiUrl="/chatbot" /> */}
            <header className='bg-gray-800 h-20 flex items-center'>
                <strong className='text-3xl font-bold italic text-white ml-10 cursor-pointer' onClick={goHome}>LAREDO</strong>
                <CustomButton className='ml-auto mr-10' onClick={goModels}>Show available models</CustomButton>
            </header>
            { !hasStarted ?
                <div className='flex flex-col items-center justify-center'>
                    <h1 className='text-7xl font-bold text-center mt-12'>Welcome to model creation</h1>
                    <p className='text-xl text-center mt-6'>Start by defining your model's creation type, name and selecting its problem type</p>
                    <div className="flex flex-col items-start justify-center mt-12 w-min">
                        <label className="text-2xl text-white mb-1">Creation type:</label>
                        <div className='flex justify-center items-center'>
                            <button onClick={() => setCreationType(CreationTypes.Basic)} className={`border rounded-l-3xl border-white ${creationType == CreationTypes.Basic 
                                ? activeButtonStyle 
                                : inactiveButtonStyle}`}>
                                Basic
                            </button>
                            <button onClick={() => setCreationType(CreationTypes.Advanced)} className={`border rounded-r-3xl border-white ${creationType == CreationTypes.Advanced 
                                ? activeButtonStyle 
                                : inactiveButtonStyle}`}>
                                Advanced
                            </button>
                        </div>

                        <label htmlFor="modelName" className="text-2xl text-white mb-1 mt-8">Name:</label>
                        <input 
                            id="modelName"
                            className='border border-white rounded-sm bg-gray-800 text-lg text-white p-1 h-9 w-full'
                            type="text" 
                            placeholder="Enter your model's name..."
                            value={modelName}
                            onChange={(event) => setModelName(event.target.value)}
                        />
                        {modelNameError && <p className="text-red-500 mt-2">{modelNameError}</p>}

                        <label htmlFor="problemType" className="text-2xl text-white mb-1 mt-8">Problem type:</label>
                        <select 
                            id="problemType" 
                            className='text-lg text-white rounded-sm border border-white bg-gray-800 p-1 h-9 w-full'
                            value={problemType}
                            onChange={(event) => setProblemType(event.target.value)}
                        >
                            <option className='text-lg' value="">Select a problem type...</option>
                            {problemTypes.map((problemType, index) => (
                                <option className='text-lg' key={index} value={problemType}>{problemType}</option>
                            ))}
                        </select>
                        {problemTypeError && <p className="text-red-500 mt-2">{problemTypeError}</p>}

                    </div>

                    <CustomButton onClick={handleHasStarted} className='mt-16'>Start</CustomButton>
                </div>                    
            :
                <div className='flex justify-center mt-3'>
                    <div className='inline-flex w-3/4'>
                    <button className={`flex-1 border-2 rounded-l-lg ${activeButton === Steps.Dataset 
                            ? activeButtonStyle 
                            : inactiveButtonStyle}`}
                            onClick={() => handleActive(Steps.Dataset)}>
                            {Steps.Dataset}
                        </button>
                        { creationType != CreationTypes.Basic && (
                            <button className={`flex-1 border-2 border-l-0 ${activeButton === Steps.Preprocessing 
                                ? activeButtonStyle 
                                : inactiveButtonStyle}`}
                                onClick={() => handleActive(Steps.Preprocessing)}>
                                {Steps.Preprocessing}
                            </button>
                        )}
                        <button className={`flex-1 border-2 border-l-0 ${activeButton === Steps.Algorithm 
                            ? activeButtonStyle 
                            : inactiveButtonStyle}`}
                            onClick={() => handleActive(Steps.Algorithm)}>
                            {Steps.Algorithm}
                        </button>
                        <button className={`flex-1 border-2 border-l-0 rounded-r-lg ${activeButton === Steps.Evaluation 
                            ? activeButtonStyle 
                            : inactiveButtonStyle}`}
                            onClick={() => handleActive(Steps.Evaluation)}>
                            {Steps.Evaluation}
                        </button>
                    </div>
                </div>
            }
            {activeButton === Steps.Dataset && 
                <DatasetUploading 
                    datasetFile={datasetFile}
                    setDatasetFile={setDatasetFile}
                    columnsDataType={columnsDataType}
                    setColumnsDataType={setColumnsDataType}
                    preview={preview}
                    setPreview={setPreview}
                    datasetUploaded={datasetUploaded}
                    setDatasetUploaded={setDatasetUploaded}
                    columns={columns}
                    setColumns={setColumns}
                    hasHeader={hasHeader}
                    setHasHeader={setHasHeader}
                    columnsTypeIndicated={columnsTypeIndicated}
                    setColumnsTypeIndicated={setColumnsTypeIndicated}
                    target={target}
                    setTarget={setTarget}
                    onNextStep={handleNextStep}
                />
            }
            {activeButton === Steps.Preprocessing && 
                <DatasetPreprocessing 
                    columns={columns}
                    columnsDropSelected={columnsDropSelected}
                    setColumnsDropSelected={setColumnsDropSelected}
                    dropColumns={dropColumns}
                    setDropColumns={setDropColumns}
                    selectedMethods={preprocessingMethods}
                    setSelectedMethods={setPreprocessingMethods}
                    onNextStep={handleNextStep}
                />
            }
            {activeButton === Steps.Algorithm && 
                <ModelSelection
                    CreationTypes={CreationTypes}
                    creationType={creationType} 
                    problemTypeEvalMetrics={BasicProblemTypesEvalMetrics[problemType]}
                    evalMetric={evalMetric}
                    setEvalMetric={setEvalMetric}
                    preset={preset}
                    setPreset={setPreset}
                    timeLimit={timeLimit}
                    setTimeLimit={setTimeLimit}
                    algorithm={algorithm}
                    setAlgorithm={setAlgorithm}
                    parametersValue={parametersValue}
                    setParametersValue={setParametersValue}
                    problemType={problemType}  
                    onNextStep={handleNextStep}  
                />
            }
            {activeButton === Steps.Evaluation &&                 
                <>
                    {isTraining ? (
                        <div className='flex flex-col items-center justify-center h-[66vh]'>
                            <svg class="text-gray-300 animate-spin" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"
                                width="100" height="100">
                                <path
                                    d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
                                    stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path
                                    d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
                                    stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"
                                    class="text-cyan-400">

                                </path>
                            </svg>
                            <h1 className='text-5xl mt-7'>Training your model...</h1>
                            <h2 className='text-2xl mt-7 text-center mx-12'>
                                This process may take some time. If you prefer not to wait, you can view your trained model in the available models section.
                            </h2>
                        </div>
                    ) : (
                        <>
                            {metrics ? (
                                <ModelEvaluation metrics={metrics} />
                            ) : (
                                <div className='flex flex-col items-center justify-center h-[66vh]'>
                                    <h1 className='text-5xl mt-7 text-red-500'>¡Oops! Something went wrong</h1>
                                    <h2 className='text-2xl mt-7 text-white text-center mx-12'>
                                        Please check if you have correctly selected your dataset and if the preprocessing methods chosen are suitable for your dataset.
                                    </h2>
                                </div>
                            )}
                        </>
                    )}
                </>
            }
        </>
    )
}

export default ModelCreation