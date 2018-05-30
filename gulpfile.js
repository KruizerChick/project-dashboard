
////////////////////////////////
//           Setup            //
////////////////////////////////

// Plugins
var gulp = require('gulp'),
      pjson = require('./package.json'),
      // gutil = require('gulp-util'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      rename = require('gulp-rename'),
      del = require('del'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      uglify = require('gulp-uglify'),
      imagemin = require('gulp-imagemin'),
      spawn = require('child_process').spawn,
      runSequence = require('run-sequence'),
      browserSync = require('browser-sync').create(),
      reload = browserSync.reload
      watchUI = require('./project_dashboard/assets/semantic/tasks/watch'),
      buildUI = require('./project_dashboard/assets//semantic/tasks/build');


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);
  var vendorsRoot = 'node_modules/';

  return {

    app: this.app,
    source: this.app + '/assets',
    dest: this.app + '/static',
    srcUI: this.app + '/assets/semantic/src',
    distUI: this.app + '/assets/semantic/dist',
    templates: this.app + '/templates',
    sass: this.app + '/assets/sass',
    css: '/css',
    fonts: '/fonts',
    images: '/images',
    js: '/js'
  }
};

var paths = pathsConfig();

////////////////////////////////
//           Tasks            //
////////////////////////////////

// Semantic tasks
gulp.task('watch-ui', watchUI);
gulp.task('build-ui', buildUI);


// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/styling.scss')
    .pipe(sass({
      includePaths: [
        paths.sass
      ]
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 versions']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.dest + paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.dest + paths.css));
});


// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.source + paths.js + '/app.js')
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.dest + paths.js));
});


// Copy third-party styles to static folder
gulp.task('copyCSS', function() {
  return gulp.src(paths.distUI + '/*.min.css')
    .pipe(gulp.dest(paths.dest + paths.css));
});

gulp.task('copyJS', function() {
  return gulp.src(paths.distUI + '/*.min.js')
    .pipe(gulp.dest(paths.dest + paths.js));
});


// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.source + paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.dest + paths.images))
});

// Run django server
gulp.task('runServer', function(cb) {
  var cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'});
  cmd.on('close', function(code) {
    console.log('runServer exited with code ' + code);
    cb(code);
  });
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init([
        paths.dest + paths.css + "/*.css",
        paths.dest + paths.js + "*.js",
        paths.templates + '*.html'
      ], {
        proxy:  "localhost:8000"
    });
});



////////////////////////////////
//       Gulp Functions       //
////////////////////////////////

// Build
gulp.task('build', function(cb) {
  runSequence(
    'build-ui',
    'styles',
    'scripts',
    'imgCompression',
    'copyCSS',
    'copyJS'
  ), cb;
});


// Watch
gulp.task('watch', ['runServer', 'browserSync', 'watch-ui'], function() {
  gulp.watch(paths.sass + '/**/*.scss', ['styles']);
  gulp.watch(paths.source + paths.js + '/*.js', ['scripts']).on("change", reload);
  gulp.watch(paths.source + paths.images + '/*', ['imgCompression']);
  gulp.watch(paths.templates + '/**/*.html').on("change", reload);

});

// Default task
gulp.task('default', function() {
  runSequence('build', 'watch');
});
