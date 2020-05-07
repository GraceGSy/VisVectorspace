import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';

const appRoot = require('app-root-path');
const spawn = require("child_process").spawn;

const production = !process.env.ROLLUP_WATCH;

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		svelte({
			// enable run-time checks when not in production
			dev: !production,
			// we'll extract any component CSS out into
			// a separate file - better for performance
			css: css => {
				css.write('public/build/bundle.css');
			}
		}),

		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration -
		// consult the documentation for details:
		// https://github.com/rollup/plugins/tree/master/packages/commonjs
		resolve({
			browser: true,
			dedupe: ['svelte']
		}),
		commonjs(),

		// In dev mode, call `npm run start` once
		// the bundle has been generated
		!production && serve(),

		// Watch the `public` directory and refresh the
		// browser on changes when not in production
		!production && livereload('public'),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		production && terser()
	],
	watch: {
		clearScreen: false
	}
};


function runbackend() {
	console.log('------ > RUNNING BACKEND ...')
	// run base model
	let results = []
	let modelpyfile = appRoot + "/backend/modeler.py"
	let obj = {}
	let baseMod = 1
	console.log(' CHECKING APPROOT ', appRoot, modelpyfile)
	var process = spawn("python3", [modelpyfile, "-", "-"])
	process.stdout.on('data', (data) => {
		console.log('python results came back ', data.toString())
		results.push(data.toString());
	})
	process.stderr.on('data', (data) => {
		console.log(`python results error:${data}`);
	});
	process.stderr.on('close', () => {
		console.log("------- > PYTHON CALL DONE !!!! ");
	});
}

function serve() {
	let started = false;
	console.log('SERVING THROUGH CONFIG.JS ...  ')
	runbackend();

	return {
		writeBundle() {
			if (!started) {
				started = true;

				require('child_process').spawn('npm', ['run', 'start', '--', '--dev'], {
					stdio: ['ignore', 'inherit', 'inherit'],
					shell: true
				});
			}
		}
	};
}
