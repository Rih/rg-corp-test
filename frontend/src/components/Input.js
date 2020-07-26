import styled from 'styled-components'

const Input = styled.input.attrs(props => ({
  // we can define static props
  type: props.type || 'text',

  // or we can define dynamic ones
  size: "2em",
}))`
  display: flex;
  ${(({ flexDirection }) => flexDirection && `flex-direction: ${flexDirection};`)}
  ${(({ alignItems }) => alignItems && `align-items: ${alignItems};`)}
  ${(({ justifyContent }) => justifyContent && `justify-content: ${justifyContent};`)}
  height: ${(({ height }) => height ? height : 'fit-content')};
  margin: ${(({ margin }) => margin ? margin : '0')};
  padding: ${(({ padding }) => padding ? padding : '0.6rem 1rem')};
  min: ${(({ min }) => min ? min : '')};
  max: ${(({ max }) => max ? max : '')};
  background: #fff;
  border: 1px solid #ced6ea;
  border-radius: 4px
`

export default Input