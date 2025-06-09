import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import "./css/Item.css";

export class Item extends Component {
  render() {
    return (
        <div className='product-card'>
          <Link to={`/product/${this.props.item.id}`} key={this.props.item.id} className="item-link">
            <img src={this.props.item.img_main} />
            <div className='product-card__price price'>{this.props.item.price / 100} ₽</div>
            <h2 className='product-card__brand-wrap'>
                <span className='product-card__brand'>
                    {this.props.item.brand}
                </span>
                <span className='product-card__name'>
                    <span className='product-card__name-separator'> / </span>
                    {this.props.item.name}
                </span>
            </h2>
          </Link>
        </div>
    )
  }
}

export default Item