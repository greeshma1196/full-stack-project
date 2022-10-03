# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /web-scraping-project

# add `/app/node_modules/.bin` to $PATH
ENV PATH /web-scraping-project/node_modules/.bin:$PATH

# install app dependencies
COPY /web-scraping-project/package.json ./
COPY /web-scraping-project/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY /web-scraping-project .

EXPOSE 3000

# start app
CMD ["npm", "start"]