import React, { useState } from 'react'
import CustomButton from '@components/CustomButton'

const Presets = {
    MediumQuality : 'medium_quality', 
    GoodQuality : 'good_quality', 
    HighQuality : 'high_quality', 
    BestQuality : 'best_quality'
}

function BasicModelSelection({problemTypeEvalMetrics, evalMetric, setEvalMetric, preset, setPreset, timeLimit, setTimeLimit, onNextStep}) {

    const [evalMetricError, setEvalMetricError] = useState('')
    const [presetError, setPresetError] = useState('')
    const [timeLimitError, setTimeLimitError] = useState('')

    const handleNextStep = () => {
        setEvalMetricError('')
        setPresetError('')
        setTimeLimitError('')

        if (!evalMetric) {
            setEvalMetricError('Please select an evaluation metric')
        }  
        if (!preset) {
            setPresetError('Please select a preset')
        }
        if (!timeLimit || timeLimit <= 0) {
            setTimeLimitError('Please enter an execution time limit')
        }
        if (evalMetric && preset && timeLimit && timeLimit > 0) {
            onNextStep()
        }
    }

    return(
        <>
            <div className='grid grid-cols-2'>
                <div className='grid grid-cols-2 content-center items-center justify-items-end h-[80vh]'>
                    <label htmlFor="evalMetric" className="text-2xl text-white mt-8 mr-4">Evaluation Metric:</label>
                    <select 
                        id='evalMetric'
                        className='cursor-pointer text-lg text-white rounded-sm border border-white bg-gray-800 p-1 h-9 mt-8 w-full'
                        value={evalMetric} 
                        onChange={(event) => setEvalMetric(event.target.value)}
                    >
                        <option value="" disabled>Select an evaluation metric</option>
                        {problemTypeEvalMetrics.map((metric) => (
                            <option key={metric} value={metric}>
                                {metric}
                            </option>
                        ))}
                    </select>
                    {evalMetricError && <p className="col-span-2 text-red-500 mt-2">{evalMetricError}</p>}


                    <label htmlFor="preset" className="text-2xl text-white mt-8 mr-4">Preset:</label>
                    <select 
                        id='preset'
                        className='cursor-pointer text-lg text-white rounded-sm border border-white bg-gray-800 p-1 h-9 mt-8 w-full'
                        value={preset} 
                        onChange={(event) => setPreset(event.target.value)}
                    >
                        <option value="" disabled>Select a preset</option>
                        {Object.entries(Presets).map(([key, value]) => (
                            <option key={value} value={value}>
                                {key}
                            </option>
                        ))}
                    </select>
                    {presetError && <p className="col-span-2 text-red-500 mt-2">{presetError}</p>}


                    <label htmlFor="timeLimit" className="text-2xl text-white mt-8 mr-4">Time limit:</label>
                    <input 
                        id="timeLimit"
                        className='border border-white rounded-sm bg-gray-800 text-lg text-white p-1 h-9 mt-8 w-full'
                        type="text" 
                        placeholder="Enter the execution time limit..."
                        value={timeLimit}
                        onChange={(event) => setTimeLimit(Number(event.target.value))}
                    />
                    {timeLimitError && <p className="col-span-2 text-red-500 mt-2">{timeLimitError}</p>}
                </div>
                
                <div className='flex flex-col justify-start text-right mx-auto mt-40'>
                    <div className='sticky top-1/4 items-end text-right'>                    
                        <h2 className='text-5xl font-bold'>Model creation</h2>
                        <h1 className='text-6xl font-bold'>Basic</h1>
                        <strong className='mt-5'>Set this parameters to create your model.</strong>
                        <div className="ml-auto mt-6">
                            <CustomButton className='w-fit text-lg' onClick={handleNextStep}>Train your model</CustomButton>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default BasicModelSelection
