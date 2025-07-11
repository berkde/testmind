import Card from "../components/Card.jsx";
import "./Contact.css";
import loriImage from "../assets/lori.png";
import berkImage from "../assets/berk.png";
import adamImage from "../assets/adam.png";
import jiaweiImage from "../assets/jiawei.png";

const Contact = () => {
  const team = [
    {
      image: loriImage,
      title: "Lori Schmidt",
      link: "https://github.com/lms651",
      role: "Team Lead",
    },
    {
      image: berkImage,
      title: "Berk Delibalta",
      link: "https://github.com/berkde",
      role: "Lead Engineer",
    },
    {
      image: adamImage,
      title: "Adam Cebulski",
      link: "https://github.com/adamc95",
      role: "QA Engineer",
    },
    {
      image: jiaweiImage,
      title: "Jiawei Cheng",
      link: "https://github.com/jxc1687",
      role: "Frontend Engineer",
    },
  ];

  return (
    <div className="contact-container">
      <div className="contact-content">
        <h2 className="contact-title">Meet Our Team</h2>
        <div className="card-list">
          {team.map((member, index) => (
            <Card
              key={index}
              image={member.image}
              title={member.title}
              link={member.link}
              role={member.role}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Contact;
