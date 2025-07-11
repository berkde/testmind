import "./Card.css";

const Card = ({ image, title, link, role }) => {
  return (
    <div className="card">
      <div className="card-avatar">
        <img src={image} alt={title} />
      </div>
      <div className="card-content">
        <a href={link} target="_blank" className="card-title">
          {title}
        </a>
        <p className="card-role">{role}</p>
      </div>
    </div>
  );
};

export default Card;
