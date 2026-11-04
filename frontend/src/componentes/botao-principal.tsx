import './botao-principal.css'
import { useRef } from 'react'

interface BotaoPrincipalProps {
  onClick?: () => void;
  label: string;
  disabled?: boolean;
  icon?: React.ReactNode;
}

function BotaoPrincipal({ onClick, label, disabled, icon }: BotaoPrincipalProps) {
  const buttonRef = useRef<HTMLButtonElement>(null)

  return (
    <div className="botao-principal">
      <button
        ref={buttonRef}
        type="button"
        onClick={onClick}
        disabled={disabled}
      >
        {icon ? <span>{icon}</span> : null}
        <span>{label}</span>
      </button>
    </div>
  )
}

export default BotaoPrincipal