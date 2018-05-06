
var webpack = require('webpack');
var CompressionPlugin = require("compression-webpack-plugin");

console.log(__dirname)

module.exports = {
    entry: {
        main: ['./index.js']
    },
    output: {
        path: __dirname + '/../staticfiles/assets/js',
        filename: 'bundle.js'
    },
    cache: false,
    mode:'development',
    devtool: 'cheap-module-source-map',
    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': '"production"'
        }),
        new webpack.IgnorePlugin(/^\.\/locale$/, [/moment$/]),
        new webpack.NoEmitOnErrorsPlugin(),
        new CompressionPlugin({
            asset: "[path].gz[query]",
            algorithm: "gzip",
            test: /\.js$|\.css$|\.html$/,
            threshold: 10240,
            minRatio: 0
        }),new webpack.ProvidePlugin({

            Popper: ['popper.js', 'default']
        })],
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['es2015']
                        }
                    }
                }
            ]
        }
}
