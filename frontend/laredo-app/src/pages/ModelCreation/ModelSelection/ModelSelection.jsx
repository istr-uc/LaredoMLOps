import React, { useState } from 'react'
import AdvancedModelSelection from '@pages/ModelCreation/ModelSelection/AdvancedModelSelection'
import BasicModelSelection from '@pages/ModelCreation/ModelSelection/BasicModelSelection'


function ModelSelection({CreationTypes, creationType, problemTypeEvalMetrics, evalMetric, setEvalMetric, preset, setPreset, timeLimit, setTimeLimit, algorithm, setAlgorithm, parametersValue, setParametersValue, problemType, onNextStep}) {

    const [showAdvance, setShowAdvance] = useState(false)

    return(
        <>
            {creationType == CreationTypes.Advanced ? 
                <AdvancedModelSelection 
                    algorithm={algorithm}
                    setAlgorithm={setAlgorithm}
                    parametersValue={parametersValue}
                    setParametersValue={setParametersValue}
                    problemType={problemType}
                    onNextStep={onNextStep}
                /> 
                : 
                <BasicModelSelection 
                    problemTypeEvalMetrics={problemTypeEvalMetrics}
                    evalMetric={evalMetric} 
                    setEvalMetric={setEvalMetric} 
                    preset={preset} 
                    setPreset={setPreset} 
                    timeLimit={timeLimit} 
                    setTimeLimit={setTimeLimit}
                    onNextStep={onNextStep}
                />
            }
        </>
    )
}

export default ModelSelection