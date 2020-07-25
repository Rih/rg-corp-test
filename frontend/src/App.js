import React from 'react'
import { Route } from 'react-router-dom'

import ScraperView from './views/scraper/Scraper.view'

import GlobalStyles from './globalStyles'

const App = () => {
  return (
    <React.Fragment>
      <GlobalStyles />
      <Route exact path='/' component={ScraperView} />
    </React.Fragment>
  )
}

export default App
