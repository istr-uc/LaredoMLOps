import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import eyeIcon from '@assets/images/eyeIcon.png'
import CustomButton from '@components/CustomButton'
import axios from 'axios'
import affirmationIcon from '@assets/images/affirmationIcon.svg'
import negationIcon from '@assets/images/negationIcon.svg'


function Models() {

    const [models, setModels] = useState([])
    const navigate = useNavigate()


    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        try {
            
            //const apiIp = import.meta.env.VITE_API_IP
            //const apiPort = import.meta.env.VITE_API_PORT
            //const apiUrl = `http://${apiIp}:${apiPort}/models`
            const apiUrl = `/api/models`
            const response = await axios.get(apiUrl)
            const formattedData = response.data.map(model => ({
                ...model,
                creation_date: new Date(model.creation_time).toLocaleDateString()
            }))
        
            setModels(formattedData);
        } catch (error) {
            console.error('Error fetching data:', error)
        }
    }
    
    const goHome = () => {
        navigate('/')
    }

    const goDetails = (modelName) => {
        navigate(`/models/${modelName}`)
    }

    const goModelCreation = () => {
        navigate('/model-creation')
    }

    return (
        <>
            <header className='bg-gray-800 h-20 flex items-center'>
                <strong className='text-3xl font-bold italic text-white ml-10 cursor-pointer' onClick={goHome}>LAREDO</strong>
                <CustomButton className='ml-auto mr-10' onClick={goModelCreation}>Create a model</CustomButton>
            </header>
            
            <h1 className='text-7xl font-bold text-center mt-8'>Available Models</h1>

            <p className='text-lg text-center mt-6'>Currently, the repository has these models available. If you want more information click on the icon.</p>

            <table className='mx-auto mt-8 bg-gray-800 text-center items-center'>
                <thead>
                    <tr>
                        <th className='text-white px-24 py-5 border-8 border-slate-950'>Model</th>
                        <th className='text-white px-24 py-5 border-8 border-slate-950'>Version</th>
                        <th className='text-white px-9 py-5 border-8 border-slate-950'>Creation date</th>
                        <th className='text-white px-9 py-5 border-8 border-slate-950'>Is deployed?</th>
                        <th className='text-white px-9 py-5 border-8 border-slate-950'></th>
                    </tr>
                </thead>
                <tbody>
                    {models.map((model) => (
                        <tr key={model.model_name}>
                            <td className='font-bold px-9 py-5 border-8 border-slate-950'>{model.model_name}</td>
                            <td className='px-9 py-5 border-8 border-slate-950'>Version {model.version}</td>
                            <td className='px-9 py-5 border-8 border-slate-950'>{model.creation_date}</td>
                            <td className='px-9 py-5 border-8 border-slate-950'>
                                {model.is_deployed ? (
                                    <div className='flex justify-center items-center'>
                                        <img src={affirmationIcon} alt='Affirmation icon' width='30'/>
                                    </div>
                                ) : (
                                    <div className='flex justify-center items-center'>
                                        <img src={negationIcon} alt='Negation icon' width='30'/>
                                    </div>
                                )}
                                </td>
                            <td className='px-9 py-5 border-8 border-slate-950'>
                                <div className='flex flex-col items-center group relative'>
                                    <p className='hidden absolute text-white text-xs whitespace-nowrap -top-5 group-hover:block'>
                                        Show details
                                    </p>
                                    <img src={eyeIcon} className='w-6 h-5 cursor-pointer' alt='An eye to link to details' onClick={() => goDetails(model.model_name)} />
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    )

}

export default Models
