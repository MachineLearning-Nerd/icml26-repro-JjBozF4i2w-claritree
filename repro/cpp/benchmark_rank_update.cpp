#include <Eigen/Cholesky>
#include <Eigen/Core>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>

int main() {
  using Clock = std::chrono::steady_clock;
  using Eigen::LLT;
  using Eigen::MatrixXd;
  using Eigen::VectorXd;

  std::cout << "dimension,trial,calls,nanoseconds_per_call\n";
  volatile double checksum = 0.0;
  for (int dimension : {4, 8, 16, 32, 64, 96, 128}) {
    const int calls_target = std::max(4000, 24000000 / (dimension * dimension));
    const int pairs = std::max(1, calls_target / 2);
    VectorXd update = VectorXd::LinSpaced(dimension, 0.001, 0.002);

    for (int trial = 0; trial < 5; ++trial) {
      MatrixXd base = MatrixXd::Identity(dimension, dimension) * 4.0;
      LLT<MatrixXd> factor(base);
      for (int warmup = 0; warmup < 64; ++warmup) {
        factor.rankUpdate(update, 1.0);
        factor.rankUpdate(update, -1.0);
      }

      const auto started = Clock::now();
      for (int repetition = 0; repetition < pairs; ++repetition) {
        factor.rankUpdate(update, 1.0);
        factor.rankUpdate(update, -1.0);
      }
      const auto stopped = Clock::now();
      checksum += factor.matrixL()(0, 0);
      const double nanoseconds =
          std::chrono::duration<double, std::nano>(stopped - started).count();
      std::cout << dimension << ',' << trial << ',' << (2 * pairs) << ','
                << std::setprecision(12) << nanoseconds / (2 * pairs) << '\n';
    }
  }
  if (!std::isfinite(checksum)) return 2;
  return 0;
}
