import React, { useRef, useEffect, useState } from "react";

const PipelineIframe = ({ pipelineHtml, maxHeight = 800, maxWidth = 1000 }) => {
  const iframeRef = useRef(null);
  const [height, setHeight] = useState(400);
  const [width, setWidth] = useState(1000);

  const styleInjection = `
    <style>

      .sk-top-container {
        display: flex !important;
        justify-content: center !important;
        background-color: transparent !important;
      }
      .sk-container {
        margin: 0 auto !important;
        display: inline-block !important; /* keeps the internal table structure intact */
      }
    </style>
  `;

// Combine them without nesting <html> tags
const centeredHtml = styleInjection + pipelineHtml;

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const resizeIframe = () => {
      try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        if (!doc) return;

        const contentHeight = doc.body.scrollHeight + 20;
        // const contentWidth = doc.body.scrollWidth + 20;
        const newHeight = Math.min(contentHeight, maxHeight);
        // const newWidth = Math.min(contentWidth, maxWidth);

        if (newHeight !== height) {
          setHeight(newHeight);
        }
        // if (newWidth !== width) {
        //   setWidth(newWidth);
        // }
      } catch (err) {
        console.warn("Cannot access iframe content for resizing:", err);
      }
    };

    iframe.addEventListener("load", resizeIframe);
    const interval = setInterval(resizeIframe, 500);

    return () => {
      iframe.removeEventListener("load", resizeIframe);
      clearInterval(interval);
    };
  }, [pipelineHtml, maxHeight, height]);

  return (
    <div
      style={{
        display: "flex",           // enable flex layout
        justifyContent: "center",  // horizontal centering
        alignItems: "flex-start",  // vertical alignment at top
        width: "100%",
        padding: "20px 0",
      }}
    >
      <div
        style={{
          width: "auto",
          maxWidth: `${maxWidth}px`, // limit max width
          maxHeight: `${maxHeight}px`,
          overflow: "auto",
          //border: "1px solid #ccc",
          borderRadius: "8px",
        }}
      >
        <iframe
          ref={iframeRef}
          srcDoc={centeredHtml}
          title="ML Pipeline"
          style={{
            width: "100%",
            height: `${height}px`,
            border: "none",
            transition: "height 0.3s ease",
          }}
        />
      </div>
    </div>
  );
};

export default PipelineIframe;
