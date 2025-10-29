import React from 'react'
import closeIcon from '@assets/images/closeIcon.svg'

function CustomModal({ isOpen, onClose, children }) {
  if (!isOpen) return null

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center'>
      <div className='absolute inset-0 bg-black backdrop-filter backdrop-blur-md opacity-50'></div>
      <div className='z-50 bg-slate-950 p-8 rounded-lg shadow-lg relative'>
          <img src={closeIcon} className='absolute top-2 right-2 cursor-pointer' alt='Close Icon' onClick={onClose}/>
          {children}
      </div>
    </div>
  )
}

export default CustomModal