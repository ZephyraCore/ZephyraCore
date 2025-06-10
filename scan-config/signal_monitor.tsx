import React, { useState, useEffect } from 'react'

type SignalProps = {
  inputSignal: number
}

const useSmoothing = (value: number, factor: number): number => {
  const [smoothed, setSmoothed] = useState(value)

  useEffect(() => {
    const timeout = setTimeout(() => {
      setSmoothed(prev => prev + (value - prev) * factor)
    }, 50)
    return () => clearTimeout(timeout)
  }, [value, factor])

  return smoothed
}

const SignalStrength: React.FC<SignalProps> = ({ inputSignal }) => {
  const smoothedSignal = useSmoothing(inputSignal, 0.15)
  const [level, setLevel] = useState("Unknown")

  useEffect(() => {
    if (smoothedSignal > 80) setLevel("Strong")
    else if (smoothedSignal > 50) setLevel("Moderate")
    else setLevel("Weak")
  }, [smoothedSignal])

  return (
    <div style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: 8 }}>
      <h3>Signal Monitor</h3>
      <p>Raw: {inputSignal.toFixed(2)}</p>
      <p>Smoothed: {smoothedSignal.toFixed(2)}</p>
      <p>Status: <strong>{level}</strong></p>
    </div>
  )
}

const SignalPanel: React.FC = () => {
  const [signal, setSignal] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      const randomSignal = Math.random() * 100
      setSignal(randomSignal)
    }, 1200)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ maxWidth: 400, margin: 'auto', marginTop: '3rem' }}>
      <SignalStrength inputSignal={signal} />
    </div>
  )
}

export default SignalPanel
