import { useNavigate } from 'react-router-dom'
import CustomButton from '@components/CustomButton'
import robot from '@assets/images/robot.png'
import uc from '@assets/images/UC_LogotipoVReducida-02_blanco.png'

function Home() {

  const navigate = useNavigate()
  
  const goModelCreation = () => {
    navigate('/model-creation')
  }

  const goModels = () => {
      navigate('/models')
  }

  return (
    <div className='grid h-screen w-screen grid-cols-3 min-w-[1350px] min-h-[720px]'>
      <div className='col-span-2 flex flex-col h-full'>
        <div className='flex flex-col justify-center mx-auto grow-6'>
          <h1 className='text-[14rem] text text font-bold italic text-white -mt-24'>LAREDO</h1>
          <p className='text-[2.5rem] text-cyan-400 -mt-4'>
            Predict the future with confidence: <br/>
            Create and Apply Predictive Models intuitively.
          </p>
          <div className='flex mt-8'>
            <CustomButton onClick={goModelCreation}>Create a model</CustomButton>
            <CustomButton className='ml-4' onClick={goModels}>Show available models</CustomButton>
          </div>
        </div>
        <div className='flex justify-center w-screen grow-1'>
          <div className='flex items-center h-min'>
            <img src={uc} alt='UC logo' className='h-12'></img>
            <p className='text-white my-auto'>
              Copyright © Universidad de Cantabria, 2025
            </p>
          </div>
        </div>
      </div>
      <div className='flex items-center justify-end'>
        <img src={robot} alt='A robot for home page' className='h-screen' />
      </div>
    </div>
  )
}

export default Home
