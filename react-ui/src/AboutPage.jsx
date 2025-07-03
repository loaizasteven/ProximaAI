import React from 'react';
import ChromaGrid from './ChromaGrid'

const AboutPage = () => {
  const items = [
    {
      image: "https://avatars.githubusercontent.com/u/176247779?v=4",
      title: "Steven Loaiza",
      subtitle: "Founder/ML Engineer",
      handle: "@stevenloaiza",
      borderColor: "#3B82F6",
      gradient: "linear-gradient(145deg, #3B82F6, #000)",
      url: "https://www.linkedin.com/in/stevenloaiza"
    },
    {
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        title: "TBD",
        subtitle: "Founding AI Developer",
        handle: "@tbd",
        borderColor: "#3B82F6",
        gradient: "linear-gradient(145deg, #3B82F6, #000)",
        url: "https://www.linkedin.com/in/stevenloaiza"
      }
  ];

  return (
    <>
      <h2>
        Meet our Founding Members
      </h2>
      
      <div style={{ height: '600px', position: 'relative' }}>
        <ChromaGrid 
          items={items}
          radius={300}
          damping={0.45}
          fadeOut={0.6}
          ease="power3.out"
        />
      </div>
    </>
  );
};
  
export default AboutPage;