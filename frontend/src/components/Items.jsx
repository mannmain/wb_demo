import React, { Component } from 'react'
import Item from './Item'
import "./css/Items.css";

export class Items extends Component {
  render() {
    return (
      <main className='main__container'>
        {this.props.items.map(el => (
            <Item key={el.id} item={el}/>
        ))}
      </main>
    )
  }
}

export default Items