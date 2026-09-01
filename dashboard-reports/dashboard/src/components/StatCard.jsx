const StatCard = ({ label, value, tone = 'neutral', meta = '' }) => {
  const tones = {
    neutral: {
      badge: 'neutral',
      accentClass: 'tone-neutral',
      indicator: 'Rate',
    },
    success: {
      badge: 'success',
      accentClass: 'tone-success',
      indicator: 'Pass',
    },
    danger: {
      badge: 'danger',
      accentClass: 'tone-danger',
      indicator: 'Alert',
    },
    accent: {
      badge: 'accent',
      accentClass: 'tone-accent',
      indicator: 'Total',
    },
  }

  const currentTone = tones[tone] || tones.neutral

  return (
    <article className={`stat-card ${currentTone.accentClass}`}>
      <div className="stat-header">
        <span className="stat-label">{label}</span>
        <span className={`stat-pill ${currentTone.badge}`}>{currentTone.indicator}</span>
      </div>
      <div className="stat-value">{value}</div>
      {meta ? <div className="stat-meta">{meta}</div> : null}
    </article>
  )
}

export default StatCard
