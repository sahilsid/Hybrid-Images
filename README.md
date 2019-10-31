# Hybrid-Images

\documentclass{bmvc2k}
 \usepackage[table,xcdraw]{xcolor}
%% Enter your paper number here for the review copy
% \bmvcreviewcopy{??}

\title{Hybrid Image Synthesis}

% Enter the paper's authors in order
% \addauthor{Name}{email/homepage}{INSTITUTION_CODE}
\addauthor{Sahil Sidheekh}{2017CSB1104}{}
%\addauthor{Petra Prof}{http://www.vision.inst.ac.uk/~pp}{1}
%\addauthor{Colin Collaborator}{colin@collaborators.com}{2}

% Enter the institutions
% \addinstitution{Name\\Address}
\addinstitution{
 Indian Institute Of Technology, Ropar
}



\runninghead{CS518 - Computer Vision }{Assignment 1 Report}

% Any macro definitions you would like to include
% These are not defined in the style file, because they don't begin
% with \bmva, so they might conflict with the user's own macros.
% The \bmvaOneDot macro adds a full stop unless there is one in the
% text already.
\def\eg{\emph{e.g}\bmvaOneDot}
\def\Eg{\emph{E.g}\bmvaOneDot}
\def\etal{\emph{et al}\bmvaOneDot}

%------------------------------------------------------------------------- 
% Document starts here
\begin{document}

\maketitle

\begin{abstract}
This document demonstrates the observations and results of synthesizing hybrid images using {\bf first principles}, in {\bf python} .This work consists of two parts - Implementing an image filter applier using convolution(correlation) and then using this to filter out low frequency and high frequency components of an image which are later combined to form the hybrid image.

\end{abstract}

%------------------------------------------------------------------------- 
\section{Introduction}
\label{sec:intro}
Convolution of images with kernels in-order to enhance image properties as per user needs is a popular approach used in image processing. It is a form of linear filtering in which the value of a pixel also depends on its neighbour pixels. Depending on the values of the kernel pixels and its size, the convolution results in different features of the image being enhanced. It is also used widely today in Convolutional Neural Networks (CNNs) for the extraction of features from images, where the kernel pixel values are learned by the network, in contrast to image processing where the kernel values are set to capture a particular feature.
In this work, we use this method to extract different features of an image which are later combined as given in the paper \cite{oliva2006hybrid} to form a hybrid image - one that creates the illusion, in the viewer, of being a different entity when viewed from different distances. 
\section{Theory and Intuition}

\subsection{Image Filtering Using Convolution}
Image filtering is a process of modifying images in-order to enhance certain features/properties present in it. A linear spatial operation called {\em Convolution} is used in achieving the same, where the output pixel values are determined as the sum of the products the corresponding pixels of the image and the kernel(filter), with the kernel centered on the pixel whose output value is to be determined. Mathematically, the convolution is obtained as : 


\begin{equation*}
I[x,y]*K[x,y]=
{
\sum_{n_1=-\infty}^{\infty}\sum_{n_2=-\infty}^{\infty}I[n_1,n_2].K[x-n_1,y-n_2]
}
\end{equation*}
\begin{figure}
\begin{comment}
\begin{tabular}{ccc}
%\bmvaHangBox{\fbox{\parbox{2.7cm}{~\\[2.8mm]
%\rule{0pt}{1ex}\hspace{2.24mm}\includegraphics[width=2.33cm]{images/eg1_largeprint.png}\\[-0.1pt]}}}&
%\bmvaHangBox{\fbox{\includegraphics[width=2.8cm]{images/eg1_largeprint.png}}}&
\end{tabular}
\end{comment}
\begin{center}
\bmvaHangBox{\fbox{\includegraphics[width=9.6cm]{conv.png}}}\\ 
\end{center}
\caption{ An illustration of a 2D convolution }
\label{fig:teaser}
\end{figure}

The output pixel value is thus obtained as a weighted sum of its neighbourhood pixels, where the weights are determined by the kernel pixel values, for e.g., a kernel whose values depict a {\em Gaussian} distribution results in a Gaussian smoothening of the input image.\\

\subsection{Hybrid Images}
The main intuition beneath the creation of hybrid images is that humans visually perceive different features of the same image at different distances. As presented in the paper by Aude Oliva\cite{oliva2006hybrid},
we focus more on high frequency components of an image when viewed from a short distance whereas the low frequency components of an image attracts visual perception at longer distances. This is the underlying principle utilized in the synthesis of the hybrid images here.\\
Given two spatially similar images of two different entities, we use the image filtering technique discussed above to obtain the low frequency component of one image and the high frequency component of the second image, with the help of a low pass filter and a high pass filter. The low pass filter we use in this work is a Gaussian filter. The high frequency component is obtained by subtracting the low frequency component of an image from itself. \\ \\
The hybrid image \textbf{${H}$} is obtained from the images \textbf{${I_1}$} and \textbf{${I_2}$} , using a Gaussian filter \textbf{${G}$} as:
\begin{equation*}
H = I_1.G + I_2.(1-G)
\end{equation*}

\section{Implementation}

The implementation is in python and consists of the following 3 major modules : 


\ \ \ \ ${my\_imfilter.py}$ - that takes as input any arbitrary sized image and a filter of odd size and returns the filtered image as output, by performing a convolution using first principles. The module supports both ${RGB}$ as well as ${Grayscale}$ images. In-order to maintain the resolution of the output image, the input image is \textbf{zero padded} relative to the size of the kernel. \\ 

\ \ \ \ ${proj1.py}$ - that generates hybrid images of the inputs by generating suitable Gaussian filter for each pair of images to be hybridized and saves the plot.\\ 

\ \ \ \ ${vis\_hybrid\_image.py}$ -  that accepts a hybrid image as inputs and generates several down-scaled versions of it so that the change in interpretation is observable.\\ 

\section{Results and Observations}

The hybrid images were generated for each compatible pair of given input images, and all different configurations were experimented, which included testing several cut off frequency for the filter used and by interchanging the low pass and high pass images. Cut of frequencies for decent hybridized images which could be interpreted differently from different distances were tabulated and chosen as the optimum cut off frequency. The optimum frequencies are tabulated in Table 1. 
\\
The kernel size was set to ${(4*cut\_off\_frequency + 1)}$ x ${(4*cut\_off\_frequency + 1)}$. 
Thus varying the cut off frequency also resulted in varying kernel size thus causing variations in the amount of blurring in the low pass output and corresponding inverse variation in the high pass output. 
As different pairs of compatible images were diverse in their features and properties, it is thus expected that different personalized cut off frequency of the filter would be needed for each pair.

It was also observed that the High Pass image outputs were becoming much noisier as the cutoff frequency was increased.
\\
The hybrid images thus generated could be perceived to be different entities when scaled down (equivalent to viewing from distance). The results are given in figures 2-11 and are easily verifiable.

% Please add the following required packages to your document preamble:
% \usepackage[table,xcdraw]{xcolor}
% If you use beamer only pass "xcolor=table" option, i.e. \documentclass[xcolor=table]{beamer}
\begin{table}[]

\begin{center}
\begin{tabular}{|c|c|c|c|}
\hline
\rowcolor[HTML]{010066} 
{\color[HTML]{FFFFFF} \textbf{\begin{tabular}[c]{@{}c@{}}Low Pass\\ Image\end{tabular}}} & {\color[HTML]{FFFFFF} \textbf{\begin{tabular}[c]{@{}c@{}}High Pass \\ Image\end{tabular}}} & {\color[HTML]{FFFFFF} \textbf{\begin{tabular}[c]{@{}c@{}}Cut off Frequency \\ Used\end{tabular}}} & {\color[HTML]{FFFFFF} \textbf{\begin{tabular}[c]{@{}c@{}}Kernel \\ Size\end{tabular}}} \\ \hline
\rowcolor[HTML]{FFFFFF} 
{\color[HTML]{330001} Cat}                                                               & {\color[HTML]{330001} Dog}                                                                 & {\color[HTML]{330001} 12}                                                                         & {\color[HTML]{330001} 49 x 49}                                                         \\ \hline
\rowcolor[HTML]{FFFFFF} 
{\color[HTML]{330001} Dog}                                                               & {\color[HTML]{330001} Cat}                                                                 & {\color[HTML]{330001} 7}                                                                          & {\color[HTML]{330001} 29 x 29}                                                         \\ \hline
\rowcolor[HTML]{EFEFEF} 
{\color[HTML]{330001} Bird}                                                              & {\color[HTML]{330001} Plane}                                                               & {\color[HTML]{330001} 4}                                                                          & {\color[HTML]{330001} 17 x 17}                                                                \\ \hline
\rowcolor[HTML]{EFEFEF} 
{\color[HTML]{330001} Plane}                                                             & {\color[HTML]{330001} Bird}                                                                & {\color[HTML]{330001} 6}                                                                          & {\color[HTML]{330001} 25 x 25}                                                         \\ \hline
\rowcolor[HTML]{FFFFFF} 
{\color[HTML]{330001} Bicycle}                                                           & {\color[HTML]{330001} Motorcycle}                                                          & {\color[HTML]{330001} 7}                                                                          & {\color[HTML]{330001} 29 x 29}                                                         \\ \hline
\rowcolor[HTML]{FFFFFF} 
{\color[HTML]{330001} Motorcycle}                                                        & {\color[HTML]{330001} Bicycle}                                                             & {\color[HTML]{330001} 6}                                                                           & {\color[HTML]{330001} 25 x 25}                                                         \\ \hline
\rowcolor[HTML]{EFEFEF} 
{\color[HTML]{330001} Einstein}                                                          & {\color[HTML]{330001} Marilyn}                                                             & {\color[HTML]{330001} 3}                                                                          & {\color[HTML]{330001} 13 x 13}                                                         \\ \hline
\rowcolor[HTML]{EFEFEF} 
{\color[HTML]{330001} Marilyn}                                                           & {\color[HTML]{330001} Einstein}                                                            & {\color[HTML]{330001} 4}                                                                          & {\color[HTML]{330001} 17 x 17}                                                         \\ \hline
\rowcolor[HTML]{FFFFFF} 
Fish                                                                                     & Submarine                                                                                  & 5                                                                                                 & 21 x 21                                                                                \\ \hline
\rowcolor[HTML]{FFFFFF} 
Submarine                                                                                & Fish                                                                                       & 3                                                                                                 & 13 x 13                                                                                \\ \hline
\end{tabular}
\end{center}
\caption{\\Experimentally determined cutoff frequencies used to generate the gaussian filters}
\end{table}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/1.png}}
\end{center}
   \caption{Hybridizing Dog(Low Pass) and Cat(High Pass)}
\label{fig:short}
\end{figure*}


\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/2.png}}
\end{center}
   \caption{Hybridizing Cat(Low Pass) and Dog(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/3.png}}
\end{center}
   \caption{Hybridizing Bird(Low Pass) and Plane(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/4.png}}
\end{center}
   \caption{Hybridizing Plane(Low Pass) and Bird(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/5.png}}
\end{center}
   \caption{Hybridizing Fish(Low Pass) and Submarine(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/6.png}}
\end{center}
   \caption{Hybridizing Submarine(Low Pass) and Fish(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/7.png}}
\end{center}
   \caption{Hybridizing Bicycle(Low Pass) and Motorcycle(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/8.png}}
\end{center}
   \caption{Hybridizing Motorcycle(Low Pass) and Bicycle(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/9.png}}
\end{center}
   \caption{Hybridizing Marilyn(Low Pass) and Einstein(High Pass)}
\label{fig:short}
\end{figure*}

\begin{figure*}
\begin{center}
\fbox{\includegraphics[width=9.6cm]{Results/10.png}}
\end{center}
   \caption{Hybridizing Einstein(Low Pass) and Marilyn(High Pass)}
\label{fig:short}
\end{figure*}





\bibliography{egbib}
\end{document}
